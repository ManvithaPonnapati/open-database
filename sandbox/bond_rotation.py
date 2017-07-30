import openbabel as ob
import numpy as np

class mol:

    def __init__(self, file_path):
        '''
        Load and prepare ligand

        file_path:: path of the input pdb
        '''
        self.fPath = file_path
        self.read(file_path)
        self.get_bonds()
        self.get_atom_group()
        self.get_branch_group()
        self.get_atom_mask()
        self.get_atom_coord()
        self.get_rotate_vector()

    def rotate(self, bidx, rot_ang, side):
        '''
        Rotate ligand

        bidx:: id for the rotate bond
        rot_ang:: rotation angle
        side:: 0 or 1 since rotate bond divide ligand into 2
        '''
        T, T_ = self.get_translation_mat(self.starts[bidx])
        rot_mat = self.rotate_on_ori(self.unit_vectors[bidx], rot_ang)
        
        trans_1 = np.transpose(np.dot(T, np.transpose(self.ext_coords)))
        trans_2 = np.transpose(np.dot(rot_mat, np.transpose(trans_1)))
        trans_3 = np.transpose(np.dot(T_, np.transpose(trans_2))[:3])
        
        side_mask = (self.rotate_masks[bidx].reshape(-1,1) == side).astype(np.float)
        rotated = side_mask * trans_3 + ( 1 - side_mask ) * self.coords 
        
        return rotated
 
    def read(self, file_path):
        '''
        Read pdb file by openbabel

        file_path:: path of the input pdb
        '''
        obConversion = ob.OBConversion()
        self.obmol = ob.OBMol()
        read = obConversion.ReadFile(self.obmol, file_path)
        if read == False:
            raise Exception("Cannot read {}".format(file_path))

    def get_bonds(self):
        '''
        Find the rotable bonds in ligand
        

        '''
        rot_bond = 0
        c = 0
        rot_bonds = []
        all_bonds = []
        for bond in ob.OBMolBondIter(self.obmol):
            atom_pair =[bond.GetBeginAtomIdx()-1, bond.GetEndAtomIdx()-1]
            atom_pair = tuple(sorted(atom_pair))
            all_bonds.append(atom_pair)
            #print (not bond.IsSingle(), bond.IsAmide(), bond.IsInRing())
            #print (bond.GetBeginAtom().GetValence(), bond.GetEndAtom().GetValence())
            if not bond.IsSingle() or bond.IsAmide() or bond.IsInRing():
                c +=1
                continue
            elif bond.GetBeginAtom().GetValence() ==1 or bond.GetEndAtom().GetValence() ==1:
                c +=1
                continue
            else:

                rot_bonds.append(atom_pair)
                c +=1
                rot_bond += 1
        
        self.rot_bonds = rot_bonds
        self.all_bonds = all_bonds

    
    def dfs_split(self, idx, bidx):
        '''
        Split ligand into different rigid body

        idx:: id for the atom linked by the bond
        bidx:: id for current branch

        '''
        self.branch[idx] = bidx

        bonds = filter(lambda x:x[0]==idx or x[1]==idx, self.all_bonds)
        for bond in bonds:
            if bond[0]==idx:
                begin = bond[0]
                end = bond[1]
            else:
                begin = bond[1]
                end = bond[0]

            if self.branch[end]>=0:
                    continue
            else:
                if bond in self.rot_bonds:
                    n_bidx = max(self.branch)+1
                    self.branch_bonds.append(tuple(sorted([bidx,n_bidx])))
                    self.branch_rot_bonds.append(bond)
                    self.dfs_split(end, n_bidx)
                else:
                    self.dfs_split(end, bidx)

    def get_atom_group(self):
        '''
        Split ligand into different rigid body
        '''

        self.branch = [-1] * self.obmol.NumAtoms()
        self.branch_bonds = []
        self.branch_rot_bonds = []
        
        self.dfs_split(0,0)

        
    def label_branch(self, midx, bidx, label, rotbond):
        '''
        Divide branchs by rotable bonds

        midx:: id for current rotable bond
        bidx:: id for current branch
        label:: 0 or 1 since rotable bond divide ligand into 2 parts
        rotbond:: tuple current rotable bond
        '''
        self.branch_mask[midx][bidx] = label
        bonds = filter(lambda x:x[0]==bidx or x[1]==bidx, self.branch_bonds)
        for bond in bonds:
            if bond == rotbond:
                continue

            if bond[0] == bidx:
                begin = bond[0]
                end = bond[1]
            else:
                begin = bond[1]
                end = bond[0]

            if self.branch_mask[midx][end] >= 0:
                continue

            self.branch_mask[midx][end] = label

            self.label_branch(midx, end, label, rotbond)

        
        
    def get_branch_group(self):
        '''
        Divide branchs by rotable bonds

        '''
        self.branch_mask = np.ones((len(self.rot_bonds), len(set(self.branch)))) * -1
        for i, bond in enumerate(self.branch_bonds):
            self.label_branch(i, bond[0], 0, bond)
            self.label_branch(i, bond[1], 1, bond)

    def get_atom_mask(self):
        '''
        Divide atoms group by rotable bonds

        '''
        self.atom_mask = np.ones((len(self.rot_bonds), self.obmol.NumAtoms())) * -1
        
        for i, b_mask in enumerate(self.branch_mask):
            for bidx in np.where(self.branch_mask[i]==0)[0]:
                self.atom_mask[i][np.where(self.branch == bidx)] = 0
            for bidx in np.where(self.branch_mask[i]==1)[0]:
                self.atom_mask[i][np.where(self.branch == bidx)] = 1

    def get_atom_coord(self):
        '''
        Get coordinate of the atoms

        '''
        coords = []
        for obatom in ob.OBMolAtomIter(self.obmol):
            coords.append([obatom.x(), obatom.y(), obatom.z()])
        
        self.coords = np.asarray(coords)
        self.ext_coords = np.hstack((coords,np.ones((self.coords.shape[0],1))))

    def get_rotate_vector(self):
        '''
        Prepare rotate vector and rotate atom mask for all rotable bonds

        '''
        unit_vectors = []
        starts = []
        rotate_masks =[]
        for rbidx, bond in enumerate(self.branch_rot_bonds):
            vector = self.coords[bond[0]] - self.coords[bond[1]]
            unit_vector = vector/ np.sqrt(np.sum(np.square(vector),axis=-1))
            start = self.coords[bond[0]]
            
            mask = self.atom_mask[rbidx]

            unit_vectors.append(unit_vector)
            starts.append(start)
            rotate_masks.append(mask)
            
        self.unit_vectors = unit_vectors
        self.starts = starts
        self.rotate_masks = rotate_masks

    def get_translation_mat(self, origin):
        '''
        Prepare matrix shifts between origin point and (0,0,0)

        '''
        T = np.asarray([
            [1,0,0, -origin[0]],
            [0,1,0, -origin[1]],
            [0,0,1, -origin[2]],
            [0,0,0, 1]
        ])

        T_ = np.asarray([
            [1,0,0, origin[0]],
            [0,1,0, origin[1]],
            [0,0,1, origin[2]],
            [0,0,0,1]
        ])
        
        return T, T_

    def rotate_on_ori(self, vec, theta):
        '''
        Prepare matrix rotate along vec 

        '''
        cos = np.cos
        sin = np.sin
        u,v,w = vec[0], vec[1], vec[2]

        rotmat = [
            [
                u**2 + (1-u**2)*cos(theta),
                u*v*(1-cos(theta)) - w*sin(theta),
                u*w*(1-cos(theta)) + v*sin(theta),
                0
            ],
            [
                u*v*(1-cos(theta)) + w*sin(theta),
                v**2 + (1-v**2)*cos(theta),
                v*w*(1-cos(theta)) - u*sin(theta),
                0
            ],
            [
                u*w*(1-cos(theta)) - v*sin(theta),
                v*w*(1-cos(theta)) + u*sin(theta),
                w**2 + (1-w**2)*cos(theta),
                0
            ],
            [
                0,
                0,
                0,
                1
            ]
        ]

        rotmat = np.asarray(rotmat)
        return rotmat
   

if __name__ == '__main__':
    # read pdb file 'ligand.pdb'
    ligand = mol('ligand.pdb')
    # rotate along first rotable bond, rotation angle is 1 rad, rotate the latter part of the ligand
    rotated_coord = ligand.rotate(0, 1, 1)
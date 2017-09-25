import sys

class Test_img_init:
    this_module = sys.modules[__name__]
    def __init__(self):
        self.this_module.test_img_init = self

def test_img(init="test_img_init"):
    """
    Example to add image into api doc
    
    <b>Rmsd Distribution for Vinardo Docking result</b>
    <img src="images/vinardo_rmsd.png">

    """

    return None

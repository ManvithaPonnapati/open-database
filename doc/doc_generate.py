import os,sys
import inspect



class MHTML:
    
    def __init__(self):
        self.mod_dict = {}
        self.parsed = []
        self.github_dir = 'https://github.com/mitaffinity/open-database/tree/master/affinityDB/'
        

        # html header load css and some js script
        self.head = '''
        <!DOCTYPE html>
<html>

<head>
  <!--Import Google Icon Font-->
  <link href="http://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
  <!--Import materialize.css-->
  <link type="text/css" rel="stylesheet" href="stylesheets/materialize.min.css" media="screen,projection" />
    
    
  <link type="text/css" rel="stylesheet" href="stylesheets/style.css">
  <link type="text/css" rel="stylesheet" href="stylesheets/default.css">
  <script type="text/javascript" src="js/highlight.pack.js"></script>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

<script>hljs.initHighlightingOnLoad();</script>
    
  <!--Let browser know website is optimized for mobile-->
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <!-- UDF CSS -->
  <link rel="stylesheet" href="stylesheets/plot.css" type="text/css">
</head>

        '''

        # html javescript 
        self.js = '''
        
<!--Import jQuery before materialize.js-->
<script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
<script type="text/javascript" src="js/materialize.min.js"></script>

<!-- Init JS component for materialize     -->
    <script>hljs.initHighlightingOnLoad();</script>
<script>
   function show_doc(obj){
    
     var idx = $(obj).attr("href").substr(1);
     
     var cards = $(".cube")


     for (var i=0;i<cards.length;i++){
      if (cards[i].id==idx){
        $(cards[i]).css('display','block');
      }
      else{
        $(cards[i]).css('display','none');
      }
     }
     
          var as = $(".table-of-contents a");
     for (var i=0;i<as.length;i++){
       if (as[i] == obj){
         $(as[i]).attr("class","active");

       }
       else{
          $(as[i]).attr("class","");
       }
     }
     
     

  }
</script>
<script>
    $(document).ready(function () {
        $('ul.tabs').tabs();
    });
    
    
  // Initialize collapse button
  $(".button-collapse").sideNav();
  // Initialize collapsible (uncomment the line below if you use the dropdown variation)
  //$('.collapsible').collapsible();
    
      $(document).ready(function(){
    $('.collapsible').collapsible();
  });
  
  $(document).ready(function(){
      $('.cube').css('display','none');
      $('#index').css('display','block');
  })

</script>
<!-- D3 Js -->
<script src="https://d3js.org/d3.v4.min.js"></script>
<!-- User defined Js function -->
<script src="js/plot.js"></script>
<!-- Getting data and plot curve  -->
<script>
    var xData = [0.2, 0.3, 0.5, 0.6, 0.7, 0.8];
    var yData = [0.4, 0.6, 0.7, 0.5, 0.9, 0.2];
    var data = zip_data(xData, yData);

    d3.csv('data/data.csv',function(data){
        plot_roc(data)

    })
    //        plot_roc(data);
</script>
</body>

</html>
        '''
        
    def _div(self):
        return '\n<div class="divider"></div>\n'
    
    def _wrap(self, val,label, cls=None, ids=None, href=None, nline=True, dic = None):
        """
        wrap content in html dom

        """
        cls_str = ''
        ids_str = ''
        href_str = ''
        dic_str = ''
        if cls is not None:
            cls_str = ' class="'+cls+'" '
        if ids is not None:
            ids_str = ' id="'+ids+'" '
        if href is not None:
            href_str = ' href="'+href+'"'
        if dic is not None:
            for key in dic.keys():
                dic_str += ' {}="{}" '.format(key, dic[key])
            
        if nline:
            return '<' + label + cls_str + ids_str + href_str + dic_str + '>' + val + '</'+label+'>\n'
        else:
            return '<' + label + cls_str + ids_str + href_str + dic_str + '>' + val + '</'+label+'>'
        
        
    def _card(self, title, cont,cls=None,idx=None):
        """
        wrap content inside card obj
        """
        cls_str = ''
        if cls is not None:
            cls_str = cls
            
        idx_str = ''
        if idx is not None:
            idx_str = 'id="'+idx+'"'
        
        temp = '''
        <div class="row {}" {}>
          <div class="col s12 m12">
            <div class="card scrollspy " >
              <div class="card-content">
                <span class="card-title">{}</span>
                  {}
              </div>
            </div>
          </div>
        </div>
        '''
        
        return temp.format(cls_str, idx_str, title, cont)
    
    def _icon(self, val):
        return 
    
    def get_func_path(self, func):
        mod_name = func.__module__
        mod = eval(mod_name)
        mod_fpath = mod.__file__.replace('.pyc','.py')
        return mod_fpath
    
    def parse_doc(self, doc):
        """
        parse doc string 

        """

        des = []
        exp = []
        out = []
        par = []
        ret = []
        des_flag = True
        exp_falg = True
        out_flag = True
        par_flag = True
        ret_flag = True
        
        if doc is None:
            return ''
        
        # divide doc into three parts description parameter and return values
        for line in doc.split('\n'):
            if des_flag and not line.startswith(':param') and not line.startswith(':return'):
                des.append(line)
            else:
                des_flag = False
                
                if par_flag and line.startswith(':param'):
                    par.append(line)
                else:
                    par_flag = False
                    ret.append(line)
        
        # create list for input and output
        styled_par = self.stylish_par(par)
        styled_ret = self.stylish_ret(ret)
        
        if len(styled_ret) == 0:
            styled_ret = 'None'
            
        # wrap content and add title
        desc = self._wrap('<br>'.join(des),'div', cls='section')
        param_cont = self._wrap( self._wrap('Args','b') + '<br>' + styled_par,'div',cls='section')
        return_cont = self._wrap( self._wrap('Returns','b') + '<br>' + styled_ret,'div',cls='section')
        
        return '\n<div class="divider"></div>\n'.join([desc, param_cont, return_cont]) 
    
    def get_func_string(self, func):
        """
        parse the parameter name and devault value for function and method 
        """
        func_name = func.__name__
        func_code = func.__code__
        func_args = func_code.co_varnames[:func_code.co_argcount]
        defaults = func.__defaults__
        default_len  = 0 if defaults is None else len(defaults)
        n_default_len = len(func_args) - default_len
        
        func_string = '<pre lang="python">' + func_name + '(' + '\n'
        
        for i,arg in enumerate(func_args):
            if i >= n_default_len:
                func_string += '\t' + arg + '=' + str(defaults[i - n_default_len]) + ',\n'
            else:
                func_string += '\t' + arg + ',\n'
        func_string += ')</pre>\n'
        
        return func_string
            
                    

    def stylish_par(self, par):
        """
        parse input parameter as list
        """
        styled_par = []
        for p in par:
            cont = p.lstrip(':param').strip()
            sep = cont.find(':')
            key, value = cont[:sep].strip(), cont[sep+1:].strip()
            styled_par.append(self._wrap(self._wrap(self._wrap(key,'code'),'b') + ':' + value, 'li'))
        return '<ul>' + '\n'.join(styled_par) + '</ul>'
    
    def stylish_ret(self, ret):
        """
        parse return values as an item in list
        """
        styled_ret = []
        for r in ret:
            if r.startswith(':return:'):
                cont = r.lstrip(':return:').strip()
            else:
                cont = r.strip()
            if len(cont.strip())>0:
                styled_ret.append(self._wrap(cont, 'li'))
        return  '<ul>' + '\n'.join(styled_ret) + '</ul>'    
        
        
    def write(self,name_chain, name, package, func_string, func_path, doc,cls_cont, level):
            """
            convert doc_string to html format
            """
            
            # parse content
            cont = self.parse_doc(doc)
            func_link = '<br>Defined in <a href="{}">{}</a><br>'.format(os.path.join(self.github_dir, func_path), func_path)
            cont =  self._div() + func_string + func_link +  cont
            
            name = name_chain + '.' + name

            
            # save content into dict
            if package not in self.mod_dict.keys():
                self.mod_dict[package] = {'class':{}, 'func':{}}
            
            cur_dict = self.mod_dict[package]['class'] if cls_cont else self.mod_dict[package]['func']            
                    

            if not name_chain in cur_dict.keys():            
                cur_dict[name_chain] = {}
            
            cur_dict[name_chain].update({name:cont})
            

        
    def nav_index(self):
        """
        Biild side nav bar
        """
        
        colla_temp = '''
        <ul class="collapsible collapsible-accordion">
          <li class="bold">
            <a class="collapsible-header waves-effect waves-teal">{}</a>
            
            <div class="collapsible-body">
              {}
            </div>
          </li>
        </ul>

        '''
        
        nav_temp = '''
        <div class="nav-cont">
          <ul id="slide-out" class="side-nav fixed">
            <li><a class="waves-effect brand" href="#!">Affinity Api Doc</a></li>
              <li class="no-padding">
              {}
              {}
              </li>
          </ul>
        </div>
        
        '''
        
        # add button for index
        index = self._wrap('Index','a', href='#index',cls='collapsible-header', dic={'onclick':'show_doc(this)'})
        index = self._wrap(self._wrap(index,'li'),'ul')
        
        
        mod_panels = []
        for mod_key in sorted(self.mod_dict.keys()):
            panels = []
            items = []
            keys = []

            # collect all the functions and class ranked by name
            for func_key in self.mod_dict[mod_key]['func'].keys():
                keys += self.mod_dict[mod_key]['func'][func_key].keys()
            keys += self.mod_dict[mod_key]['class'].keys()
            
            # create list
            keys = sorted(keys)
            for key in keys:
                items.append(self._wrap(self._wrap(key.split('.')[-1],'a', href='#'+key,dic ={'onclick':'show_doc(this)'}),'li'))
            items_list = self._wrap('\n'.join(items),'ul',cls='section table-of-contents')
            mod_panels.append(colla_temp.format(mod_key, items_list))
                        
                        
        return nav_temp.format(index,'\n'.join(mod_panels))
                        
        
    def build_index(self):
        """
        Build index for all the functions and methods 

        """
        
        index_str = ''
        index_dict = {}
        for mod_key in sorted(self.mod_dict.keys()):
            
            mod_dict = {}
            
            for func_key in self.mod_dict[mod_key]['func'].keys():
                for key in self.mod_dict[mod_key]['func'][func_key].keys():
                    mod_dict['.'.join(key.split('.')[1:])] = key
                    #mod_dict[key.split('.')[-1]] = {'link_id':key}
            for cls_key in self.mod_dict[mod_key]['class'].keys():
                for key in self.mod_dict[mod_key]['class'][cls_key].keys():
                    mod_dict['.'.join(key.split('.')[1:])] = '.'.join(key.split('.')[:-1])
                
            index_dict[mod_key] = mod_dict
            
        for mod_key in sorted(index_dict.keys()):
            mod_str = self._wrap(mod_key, 'h2')
            li =[]
            for key in sorted(index_dict[mod_key].keys()):
                link_id = index_dict[mod_key][key]
                li.append(self._wrap(self._wrap(key,'a',href='#'+link_id,dic ={'onclick':'show_doc(this)'}),'li'))
            ul = self._wrap('\n'.join(li),'ul',cls='section table-of-contents')
            index_str += mod_str + ul
            
        
        
        return self._wrap(self._wrap('Index','h2',cls='header') + self._card('', index_str),'div', cls='cube', ids='index')
        
            
        
    def dump_html(self, path):
        """
        generate html page, and write down to the path
        """
            
        html_str = ''
        func_str = '\n'
        cls_str = '\n'
        
        for mod_key in sorted(self.mod_dict.keys()):
            pack_dict = self.mod_dict[mod_key]
            
            # generate card for function
            for sub_key in sorted(pack_dict['func'].keys()):
                sub_dict = pack_dict['func'][sub_key]

                for key in sorted(sub_dict.keys()):
                    func_str += self._card(key.split('.')[-1], sub_dict[key], cls='cube',idx=key)
                    func_str += '\n'

            # generate card for class
            for sub_key in sorted(pack_dict['class'].keys()):
                temp_str = ''
                sub_dict = pack_dict['class'][sub_key]
                temp_str += self._wrap(sub_key.split('.')[-1],'h2',cls='header')

                # card for methods inside class
                for key in sorted(sub_dict.keys()):
                    temp_str += self._card(key.split('.')[-1], sub_dict[key],idx=key)
                    temp_str += '\n'
                    
                cls_str += self._wrap(temp_str,'div',cls='cube',ids=sub_key)


            html_str += func_str + cls_str
            func_str = '\n'
            cls_str = '\n'
            
        # add index card
        html_str = self.build_index() + html_str
        
        # style
        html_str = html_str.replace('Example:', self._wrap('Example:','b'))
        html_str = html_str.replace('Output:', self._wrap('Output:','b'))
        html_str = html_str.replace('<pre lang="python">', '<pre lang="python">\n<code class="python">\n')
        html_str = html_str.replace('</pre>','</code>\n</pre>')

        # add side-nav bar
        html_str = self._wrap(self.nav_index() + self._wrap(html_str, 'div',cls='main-cont'), 'body')
        # concatenate html body with head and js
        html_str = self.head + html_str + self.js
        
        with open(path, 'w') as fout:
            fout.write(html_str)
                        
            
            
    def scan(self, mod, package, name_chain='',cls_cont=False, level=0):
        """
        iter through module to extract all doc_string

        """
        
        if len(name_chain):
            name_chain += '.'
            
        self.parsed.append(mod)
        
        for sub_mod_name in dir(mod):

            # ignore build_in mod 
            if sub_mod_name in ['__init__'] or not sub_mod_name.startswith('_') and not sub_mod_name.startswith('im_'):
                
                sub_mod = eval(name_chain+mod.__name__+'.'+sub_mod_name)
                
                # skip parsed module
                if sub_mod in self.parsed:
                    continue
                    
                # parse a class
                if type(sub_mod).__name__ in ['classobj']:
                    self.scan(sub_mod,package,name_chain+mod.__name__,True,level+1)
                    

                # parse function and method
                elif type(sub_mod).__name__ in ['instancemethod','function']:
                    if sub_mod.__module__.startswith(package):
                        doc =  inspect.getdoc(sub_mod)
                        func_string = self.get_func_string(sub_mod)
                        func_path = self.get_func_path(sub_mod)
                        self.write(name_chain +mod.__name__, sub_mod.__name__, package, func_string, func_path,doc,cls_cont, level)
                
                # parse module 
                elif type(sub_mod).__name__ in ['module']:
                    sub_package = sub_mod.__package__

                    # ignore extra module 
                    if sub_package is None or not sub_package == package:
                        pass
                       
                    else:
                        exec('import '+sub_mod.__name__)
                        self.scan(sub_mod,sub_mod.__package__,'',False,level+1)
                else:
                    continue
                    
    def parse_module(self, mod_name):
        """
        parse module under current directory
        """
        
        exec('import '+mod_name)
        
        main_mod = sys.modules[__name__]
        exec('main_mod.'+mod_name+'='+mod_name)

        mod = eval(mod_name)
        self.scan(mod, mod.__package__)
        
        mod_path = os.path.dirname(os.path.abspath(mod.__file__))
        for fname in os.listdir(mod_path):
            if fname.endswith('.py') and not fname.startswith('__'):
                sub_mod_name = mod_name + '.' + fname.split('.')[0]
                exec('import '+ sub_mod_name)
                sub_mod = eval(sub_mod_name)
                self.scan(sub_mod, sub_mod.__package__)       



if __name__ == '__main__':
    module_dir = os.path.join(os.path.dirname(os.getcwd()),'affinityDB')
    doc_dir = os.getcwd()

    os.chdir(module_dir)
    parser = MHTML()
    parser.parse_module('database')
    parser.parse_module('lib_multithread')
    parser.parse_module('lib_singlethread')
    parser.dump_html(os.path.join(doc_dir,'index.html'))
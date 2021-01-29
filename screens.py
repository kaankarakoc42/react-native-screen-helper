import sys,os,shutil
from glob import glob
rcc="""
import React, {{ Component }} from 'react';
import {{ Text, View }} from 'react-native';
import styles from './styles.js'

class {0} extends Component {{
  constructor(props) {{
    super(props);
    this.state = {{
    }};
  }}

  render() {{
    return (
      <View style={{styles.container}}>
        <Text> {0} </Text>
      </View>
    )
  }}
}}

export default {0}

                """
styles="""import {StyleSheet,Dimensions} from 'react-native';

const styles = StyleSheet.create({
  container: {
     flex:1,
     justifyContent: "center",
     alignItems: "center"
  },
});

export default styles;                
                
                """
class screens:
    def clearscreens(self):
        self.screens=[]
        for name in glob('./screens/*'):
            name=name.replace("./screens\\","") 
            if not ".js" in name :
                self.screens.append(name) 

    def setScreenName(self,name):
        screen=name.lower()
        screen=screen[0].upper()+screen[1:]
        if "screen" in screen:
            screen=screen.replace("screen","Screen")
        else:
            screen+="Screen"
        return screen

    def __init__(self):
        self.args=sys.argv
        self.path=os.getcwd()
        self.clearscreens()
        self.parser()
        
    def parser(self):
        for i in range(len(self.args)):
            if self.args[i] == "add":
                self.createScreen(self.setScreenName(self.args[i+1]))

            if self.args[i] == "fix":
                self.fixScreens()

            if self.args[i] == "del":
                self.deleteScreen(self.setScreenName(self.args[i+1]))

            if self.args[i] == "help" or len(self.args)==1:
                print("add [screen name] adds new screen") 
                print("fix [screen name] fix screens.js") 
                print("del [screen name] delete screen")          
                
    def deleteScreen(self,name):
         if os.path.exists(self.path+"/screens/"+name):
             shutil.rmtree(self.path+"/screens/"+name)
             self.fixScreens()
             print(f"[+] {name} silindi.")


    def fixScreens(self):
        self.clearscreens()
        with open(self.path+"/screens/screens.js","w") as f:
                imports="\n".join([f'import {s} from "./{s}/{s}.js"' for s in self.screens])
                exports="\n\n\nconst screens = {"+",".join(self.screens)+"}\nexport default screens;"
                screens=imports+exports
                f.write(screens)

    def control(self,name):
        for i in self.screens:
            if i == name:
                print("[-] bu isim de bir ekran zaten oluşturulmuş.")
                return False
        if os.path.exists(self.path+"/screens"):
            return True
        else:
            print(f"[-] screens dosyası bulunamadı.")
            return False
            
    def createScreen(self,name):
        if self.control(name):
            os.mkdir(self.path+"/screens/"+name)
            with open(self.path+"/screens/"+name+"/"+name+".js","w") as f:
                f.write(rcc.format(name))
            with open(self.path+"/screens/"+name+"/styles.js","w") as f:
                f.write(styles)
            self.fixScreens()
            print(f"[+] {name} oluşturuldu.")
            
app=screens()



#!/usr/bin/env python

# example colorsel.py


import pygtk
pygtk.require('2.0')
import gtk
import gobject
import random
import time
import os

from sugar.activity import activity 

a=0
b=0
add_sub=0
da=100
db=10
sec=0

cnt_answ=0
cnt_cor=0
delay=0

class LucasActivity(activity.Activity):


    def get_number(self):
        global a
        global b
        global add_sub
        global cnt_answ
        a=random.randint(1,da)
        b=random.randint(1,db)
        add_sub=random.randint(0,101) % 4
        cnt_answ=cnt_answ+1
        print a 
        print b 
        print add_sub
        if add_sub == 0:
            question="%d/%d: %d+%d" % (cnt_cor,cnt_answ,a,b)
        elif add_sub == 1:
            question="%d/%d: %d-%d" % (cnt_cor,cnt_answ,a,b)
        elif add_sub == 2:
            a=a%10
            question="%d/%d: %d*%d" % (cnt_cor,cnt_answ,a,b)
        else :
            a=random.randint(1,10)
            c=a*b
            question="%d/%d: %d:%d" % (cnt_cor,cnt_answ,c,a)
        print question
        return question

    def check_number(self,val):
        if add_sub == 0 :
            result=a+b
            self.add+=1
            self.add_td+=sec
        elif add_sub == 1 :
            result=a-b
            self.sub_td+=sec
            self.sub+=1
        elif add_sub == 2:
            result=a*b
            self.mult_td+=sec
            self.mult+=1
        else :
            c=a*b
            result=c/a
            self.div_td+=sec
            self.div+=1
        print val
        print result
        
        

        if result == int(val):
            if add_sub==0 :
                self.add_q+=1
            elif add_sub == 1:
                self.sub_q+=1
            elif add_sub == 2:
                self.mult_q+=1
            else:
                self.div_q+=1
            return True
        else:
            return False


    def tick_call(self,event):
        global sec
        global delay
        sec=sec+1
        if (delay == 1):
            if sec < 3:
                return True
            else:
                delay=0
                sec=0
        else :
            
            tmp="Total Sekunden %d Sekunden jetzt %d" % (self.total_sec,sec)
            ans.set_text(tmp)
            
            
        return True

    def enter_call(self,windget,entry):
        global sec
        global cnt_cor
        global delay
        entry_text=entry.get_text()
        if self.check_number(entry_text) == True:
            ans.set_text("Richtig")
            cnt_cor=cnt_cor+1
            
        else:
            ans.set_text("Leider Falsch")
        self.total_sec+=sec    
        sec=0
        delay=1
        quest.set_text(self.get_number())
        entry.set_text("")
#        self.window.show_all ()
#        quest.show()
#        time.sleep(3)
        return

    # Close down and exit handler
    def destroy_window(self, data=None):
        print "ende"
        app_path="%s/result.txt" % (os.path.join(activity.get_activity_root(),"data"))
        file=open(app_path,"a")
        file.write(time.strftime("%d %m %Y %H:%M:%S",time.localtime()))
        file.write(" Add %d/%d td %d" % (self.add_q,self.add,self.add_td))
        file.write(" Sub %d/%d td %d" % (self.sub_q,self.sub,self.sub_td))
        file.write(" Mul %d/%d td %d" % (self.mult_q,self.mult,self.mult_td))
        file.write(" Div %d/%d td %d" % (self.div_q,self.div,self.div_td))
        file.write("\n")
#        file.write(" add %d td %d, sub %d td %d, mult %d td %d" %(self.add,self.add_td,self.sub,self.sub_td,self.mult,self.mult_td))
        file.flush()
        file.close()
        gtk.main_quit()
        return True

    def __init__(self,handle):
        global quest,ans
        self.colorseldlg = None

	activity.Activity.__init__(self, handle)
        self._name = handle

		# Set title for our Activity
        self.set_title('gtk test')

		# Attach sugar toolbox (Share, ...)
        toolbox = activity.ActivityToolbox(self)
        self.set_toolbox(toolbox)
#        self.connect("delete_event", self.destroy_window)
        self.connect("destroy", self.destroy_window)
        toolbox.show()

       

        # Create toplevel window, set title and policies
        #window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        #window.set_title("Color selection test")
        #window.set_size_request(200,100)
        #window.set_resizable(True)

        # Attach to the "delete" and "destroy" events so we can exit
        #window.connect("delete_event", self.destroy_window)
  
        self._main_view=vbox=gtk.VBox(False,0);
        #window.add(vbox)
        vbox.show();
        
        question=self.get_number();
        print question
        quest=gtk.Label(question)
        vbox.pack_start(quest,True,True,0)
        quest.show();

        ans=gtk.Label("")
        vbox.pack_start(ans,True,True,0)
        ans.show();

        
        entry= gtk.Entry()
        entry.connect("activate",self.enter_call,entry)
	
        vbox.pack_start(entry,True,True,0)
        entry.show()
        random.seed()
       
        #window.show()
        self.add=0
        self.add_q=0
        self.sub=0
        self.sub_q=0
        self.mult=0
        self.mult_q=0
        self.div=0
        self.div_q=0
        
        self.add_td=0
        self.sub_td=0
        self.mult_td=0
        self.div_td=0
        self.total_sec=0
        self.timer=gobject.timeout_add(1000,self.tick_call,self)
	self._main_view.show()
        self.set_canvas(self._main_view)
	entry.grab_focus()
        self.show_all()

  
#def main():
#   gtk.main()
#   return 0

#if __name__ == "__main__":
#    ColorSelectionExample()
#    main()


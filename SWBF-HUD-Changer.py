#Be aware this code was written by someone that had only minor coding experience beforehand so dont expect it to be good

import tkinter as tk
from tkinter import *
from tkinter import filedialog
import json
import os
import subprocess
import shutil
from pathlib import Path
from PIL import Image, ImageTk
from tkinter import ttk

json_path = "rcs/paths.json"

def main_window():
    
    root3 = tk.Tk()
    root3.title("SWBF2 HUD Changer")

    ws = root3.winfo_screenwidth()
    hs = root3.winfo_screenheight() 

    x = (ws/3)
    y = (hs/4)

    root3.resizable(False, False)
    
    root3.geometry("600x400+%d+%d" % (x,y))
    root3.configure(bg="#333333")

    label = Label(root3, font= ("Arial", 25), text="Choose what you want to change", bg="#333333", fg="#CACACA")
    label.place(relx=0.5, rely=0.08, anchor= "center")

    def change_crosshair():
        root3.destroy()
        crosshair_window()
    
    def change_hud():
        root3.destroy()
        hud_window()

    def mod_dirs(base_path):

        #scans the users addon folder for mod maps that got a ingame.lvl under abc/data/_LVL_PC and returns them

        valid_maps = []

        if not os.path.isdir(base_path):
            return valid_maps

        for entry in os.listdir(base_path):
            project_path = os.path.join(base_path, entry)

            if not os.path.isdir(project_path):
                continue

            target_file = os.path.join(
                project_path,
                "data",
                "_LVL_PC",
                "ingame.lvl"
            )

            if os.path.isfile(target_file):
                valid_maps.append(entry)

        return sorted(valid_maps)

    def mod_selection():

        #Displays the valid mod maps in a multiple choice listbox

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        game_path = data["game_path"]

        gamedata_path = game_path.replace("\\data\\_lvl_pc", "")
        addon_path = os.path.join(gamedata_path, "addon")

        x = (ws/2.5)
        y = (hs/4)

        selection_window = tk.Toplevel(root3)
        selection_window.title("Select Mod Maps")
        selection_window.geometry("300x400+%d+%d" % (x,y))
        selection_window.configure(bg="#333333")
        selection_window.resizable(False, False)

        projects = mod_dirs(addon_path)

        frame = ttk.Frame(selection_window)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(
            frame,
            selectmode=tk.MULTIPLE,
            yscrollcommand=scrollbar.set,
            font=("Arial", 16),
            bg="#474747",
            fg="#CACACA",
            justify="center"
        )

        for project in projects:
            listbox.insert(tk.END, project)

        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        def confirm_selection():

            #saves the names of the selected mod maps in the json file

            selected_indices = listbox.curselection()
            selected_maps = [listbox.get(i) for i in selected_indices]

            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            data.pop("mod_maps", None)

            data["mod_maps"] = selected_maps

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

            for map in selected_maps:
                source_file = os.path.join(
                    addon_path,
                    map,
                    "data",
                    "_LVL_PC",
                    "ingame.lvl"
                )

                #backing up the original ingame.lvl files from the selected maps
                og_mod_dir = os.path.join("og", map)
                if  not os.path.isdir(og_mod_dir):
                    
                    os.makedirs(og_mod_dir, exist_ok=True)

                    target_file = os.path.join(og_mod_dir, "ingame.lvl")
                    shutil.copy2(source_file, target_file)

            selection_window.destroy()

        button = Button(selection_window, text="Apply", command=confirm_selection, bg="#474747", fg="#CACACA")
        button.pack(pady=5)

    def restore_og():

        #reapplies all the ingame.lvl files that were in the users game files before the SWBF HUD Changer made changes to it

        with open(json_path, "r") as f:
            data = json.load(f)
        game_path = data["game_path"]

        shutil.copy2("og/ingame.lvl", game_path)
        gamedata_path = game_path.replace("\\data\\_lvl_pc", "")

        for name in data.get("mod_maps", []):
            mod_path = os.path.join("og", name, "ingame.lvl")
            addon_path = os.path.join(gamedata_path, "addon", name, "data", "_lvl_pc")
            shutil.copy2(mod_path, addon_path)


    btn1 = Button(root3, text="Change Crosshair", command=change_crosshair, font=("Arial", 20), bg="#474747", fg="#CACACA")
    btn1.place(relx=0.5, rely=0.3, anchor="center")

    btn2 = Button(root3, text="Change HUD", command=change_hud, font=("Arial", 20), bg="#474747", fg="#CACACA")
    btn2.place(relx=0.5, rely=0.5, anchor="center")

    btn3 = Button(root3, text="Select Mod Maps", command=mod_selection, font=("Arial", 20), bg="#474747", fg="#CACACA")
    btn3.place(relx=0.5, rely=0.7, anchor="center")

    btn4 = Button(root3, text="Restore Vanilla", command=restore_og, font=("Arial", 15), bg="#474747", fg="#CACACA")
    btn4.place(relx=0.5, rely=0.9, anchor="center")

    root3.mainloop()

def hud_window():

    root4 = tk.Tk()
    root4.title("SWBF2 HUD Changer")
    ws = root4.winfo_screenwidth()
    hs = root4.winfo_screenheight() 

    x = (ws/3.5)
    y = (hs/5.4)

    root4.resizable(False, False)
    root4.geometry("800x600+%d+%d" % (x,y))
    root4.configure(bg="#333333")

    label = Label(root4, font= ("Arial", 25), text="Choose a HUD to load into your game", bg="#333333", fg="#CACACA")
    label.place(relx=0.5, rely=0.08, anchor= "center")

    hud_array = os.listdir("hud-files")
    listbox = tk.Listbox(root4, selectmode=tk.BROWSE, font=("Arial", 16), bg="#474747", fg="#CACACA", justify="center", width= 40)

    scrollbar = Scrollbar(root4, orient=VERTICAL, command=listbox.yview)
    scrollbar.place(relx=0.81, rely=0.5, anchor= "center", height= 254)

    listbox.config(yscrollcommand=scrollbar.set)

    items = hud_array
    listbox.insert(0, *items)
    listbox.place(relx=0.5, rely=0.5, anchor= "center")

    def apply_hud():

        indices = listbox.curselection()

        if not indices:
            return

        lang = listbox.get(indices)

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        game_path = data["game_path"]

        hud_folder = os.path.join("hud-files", lang)
        hud_folder = Path(hud_folder)
        hud_swap_path = os.path.join("hud-files", lang, "1playerhud.hud_")
        hud_transforms_swap_path = os.path.join("hud-files", lang, "hudtransforms.hud_")
        #copies the Hud files to a different directory otherwise the LVLTool would override the Vanilla files
        shutil.copy2(hud_swap_path, '1playerhud.hud_')  
        shutil.copy2('og/ingame.lvl', 'ingame.lvl')

        for file in hud_folder.iterdir():
            if file.name == "1playerhud.hud_":
                subprocess.run(["tools/LVLTool.exe", "-file", "ingame.lvl", "-r", "1playerhud.hud_"],creationflags=subprocess.CREATE_NO_WINDOW)

            elif file.name == "hudtransforms.hud_":
                #copies the Hud files zo a different directory otherwise the LVLTool would override the Vanilla files
                shutil.copy2(hud_transforms_swap_path, 'hudtransforms.hud_') 
                subprocess.run(["tools/LVLTool.exe", "-file", "ingame.lvl", "-r", "hudtransforms.hud_"],creationflags=subprocess.CREATE_NO_WINDOW)
                delete_transforms = "hudtransforms.hud_"
                os.remove(delete_transforms)

            else:
                #every .tga file is added and not replaced like the .hud_ files
                subprocess.run(["tools/LVLTool.exe", "-file", "ingame.lvl", "-a", file],creationflags=subprocess.CREATE_NO_WINDOW) 

        #copies the applied ingame.lvl to rcs so a different crosshair can be applied to it
        shutil.copy2('ingame.lvl', game_path)
        shutil.copy2('ingame.lvl', "rcs/ingame.lvl") 
        delete_ingame = "ingame.lvl"
        os.remove(delete_ingame)
        gamedata_path = game_path.replace("\\data\\_lvl_pc", "")
        addon_path = os.path.join(gamedata_path, "addon")

        #similar process for the mod maps but just in a loop untill every entry from the json file was applied once
        for name in data.get("mod_maps", []):
            mod_path = os.path.join("og", name, "ingame.lvl")
            shutil.copy2(mod_path, 'ingame.lvl')

            for file in hud_folder.iterdir():
                if file.name == "1playerhud.hud_":
                    subprocess.run(["tools/LVLTool.exe", "-file", "ingame.lvl", "-r", "1playerhud.hud_"],creationflags=subprocess.CREATE_NO_WINDOW)

                elif file.name == "hudtransforms.hud_":
                    shutil.copy2(hud_transforms_swap_path, 'hudtransforms.hud_')
                    subprocess.run(["tools/LVLTool.exe", "-file", "ingame.lvl", "-r", "hudtransforms.hud_"],creationflags=subprocess.CREATE_NO_WINDOW)
                    delete_transforms = "hudtransforms.hud_"
                    os.remove(delete_transforms)

                else:
                    subprocess.run(["tools/LVLTool.exe", "-file", "ingame.lvl", "-a", file],creationflags=subprocess.CREATE_NO_WINDOW)

            game_mod_path = os.path.join(addon_path, name, "data/_LVL_PC")
            shutil.copy2('ingame.lvl', game_mod_path) 
            rcs_mod_dir = os.path.join("rcs", name)

            if not os.path.isdir(rcs_mod_dir):
                os.makedirs(rcs_mod_dir, exist_ok=True)

            shutil.copy2('ingame.lvl', rcs_mod_dir)
            delete_ingame = "ingame.lvl"
            os.remove(delete_ingame)

        #deleting every file that was copied into the home directory for use with the LVLTool so keep everything organised
        delete_1playerhud = "1playerhud.hud_"
        os.remove(delete_1playerhud)  

    def import_hud():
        hud = filedialog.askdirectory(title= "Select the HUD Folder")
        if hud:

            hud = Path(hud)
            hud_folder_name = Path(hud).name

            current_dir = Path.cwd()
            create_hud_dir = os.path.join(current_dir, "hud-files", hud_folder_name)
            os.makedirs(create_hud_dir, exist_ok=True)

            for file in hud.iterdir():

                if file.name == "1playerhud.hud":

                    shutil.copy2(file, current_dir)
                    subprocess.run(["tools/ConfigMunge.exe", "-inputfile", "1playerhud.hud", "-platform", "pc", "-outputdir", create_hud_dir, "-continue"],creationflags=subprocess.CREATE_NO_WINDOW)
                    
                    #renaming the 1playerhud file otherwise the LVLTool cant replace it and copying it into hud-files to store it
                    create_hud_rename_dir = os.path.join(create_hud_dir, "1playerhud.config")
                    create_hud_rename_path = os.path.join(create_hud_dir, "1playerhud.hud_")
                    create_hud_del_dir = os.path.join(create_hud_dir, "1playerhud.config.req")
                    os.rename(create_hud_rename_dir, create_hud_rename_path)         

                    delete_munge_log = "ConfigMunge.log"
                    delete_config = "1playerhud.hud"
                    os.remove(delete_munge_log)
                    os.remove(create_hud_del_dir)
                    os.remove(delete_config)

                elif file.name == "hudtransforms.hud":

                    shutil.copy2(file, current_dir)
                    subprocess.run(["tools/ConfigMunge.exe", "-inputfile", "hudtransforms.hud", "-platform", "pc", "-outputdir", create_hud_dir, "-continue"],creationflags=subprocess.CREATE_NO_WINDOW)
                    
                    #renaming the 1playerhud fileotherwise the LVLTool cant replace it and copying it into hud-files to store it 
                    create_hud_rename_dir = os.path.join(create_hud_dir, "hudtransforms.config")
                    create_hud_rename_path = os.path.join(create_hud_dir, "hudtransforms.hud_")
                    create_hud_del_dir = os.path.join(create_hud_dir, "hudtransforms.config.req")
                    os.rename(create_hud_rename_dir, create_hud_rename_path)        

                    delete_munge_log = "ConfigMunge.log"
                    delete_config = "hudtransforms.hud"
                    os.remove(delete_munge_log)
                    os.remove(create_hud_del_dir)
                    os.remove(delete_config)
                    
                else:
                    current_dir = Path.cwd()
                    tga = file
                    tga_name = Path(tga).name
                    shutil.copy2(tga, current_dir)
                    subprocess.run(["tools/pc_TextureMunge.exe", "-inputfile", tga_name, "-platform", "pc", "-outputdir", create_hud_dir, "-continue"],creationflags=subprocess.CREATE_NO_WINDOW)
                    delete_munge_log = "pc_TextureMunge.log"
                    os.remove(tga_name)
                    os.remove(delete_munge_log)
            root4.destroy()
            hud_window()


    def delete_hud():

        indices = listbox.curselection()
        lang = listbox.get(indices)
        del_path = os.path.join("hud-files", lang)
        shutil.rmtree(del_path)

        root4.destroy()
        hud_window() 

    def switch_to_main_menu():
        root4.destroy()
        main_window()


    apply = tk.Button(root4, text="Apply HUD", command=apply_hud, bg="#474747", fg="#CACACA", font=("Arial", 16))
    apply.place(relx=0.61, rely=0.8, anchor="center")

    del1 = Button(root4, text="Delete HUD", command=delete_hud, bg="#474747", fg="#CACACA", font=("Arial", 16))
    del1.place(relx=0.39, rely=0.8, anchor="center")

    swt1 = Button(root4, text= "Main Menu", command= switch_to_main_menu, bg="#474747", fg="#CACACA", font=("Arial", 12))
    swt1.place(relx=0.058, rely=0.03, anchor="center")

    imp1 = Button(root4, text="Import HUD", command=import_hud, bg="#474747", fg="#CACACA", font=("Arial", 16))
    imp1.place(relx=0.5, rely=0.2, anchor="center")
    
    root4.mainloop()

def crosshair_window():

    root2 = tk.Tk()

    root2.title("SWBF2 HUD Changer")

    ws = root2.winfo_screenwidth()
    hs = root2.winfo_screenheight() 

    x = (ws/3.5)
    y = (hs/5.4)

    root2.resizable(False, False)

    root2.geometry("800x600+%d+%d" % (x,y))
    root2.configure(bg="#333333")

    label = Label(root2, font= ("Arial", 25), text="Choose a Crosshair to load into your game", bg="#333333", fg="#CACACA")
    label.place(relx=0.5, rely=0.08, anchor= "center")

    crosshair_array = os.listdir("crosshairs")
    listbox = tk.Listbox(root2, selectmode=tk.BROWSE, font=("Arial", 16), bg="#474747", fg="#CACACA", justify="center", width=40)

    scrollbar = Scrollbar(root2, orient=VERTICAL, command=listbox.yview)
    scrollbar.place(relx=0.81, rely=0.5, anchor= "center", height= 254)

    listbox.config(yscrollcommand=scrollbar.set)

    items = crosshair_array
    listbox.insert(0, *items)
    listbox.place(relx=0.5, rely=0.5, anchor="center")

    def apply_crosshair():
        indices = listbox.curselection()

        if not indices:
            return

        lang = listbox.get(indices)

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        game_path = data["game_path"]

        #using the rcs ingmae.lvl
        cross_swap_path = os.path.join("crosshairs", lang, "hud_bullseye.texture")
        shutil.copy2(cross_swap_path, 'hud_bullseye.texture')
        shutil.copy2('rcs/ingame.lvl', 'ingame.lvl')
        subprocess.run(["tools/LVLTool.exe", "-file", "ingame.lvl", "-r", "hud_bullseye.texture"], check=True,creationflags=subprocess.CREATE_NO_WINDOW)
        shutil.copy2('ingame.lvl', game_path)

        delete_ingame = "ingame.lvl"
        os.remove(delete_ingame)
        gamedata_path = game_path.replace("\\data\\_lvl_pc", "")
        addon_path = os.path.join(gamedata_path, "addon")

        #read the selected mod maps from the json and apply the crosshair to every one of them
        for name in data.get("mod_maps", []):
            mod_path = os.path.join("rcs", name, "ingame.lvl")
            shutil.copy2(mod_path, 'ingame.lvl')
            subprocess.run(["tools/LVLTool.exe", "-file", "ingame.lvl", "-r", "hud_bullseye.texture"],creationflags=subprocess.CREATE_NO_WINDOW)
            game_mod_path = os.path.join(addon_path, name, "data/_LVL_PC")
            shutil.copy2('ingame.lvl', game_mod_path)
            delete_ingame = "ingame.lvl"
            os.remove(delete_ingame)

        delete_cross = "hud_bullseye.texture"
        os.remove(delete_cross)


    def crosshair_import():
        crosshair = filedialog.askopenfilename(title="Select Crosshair")
        if crosshair:

            current_dir = Path.cwd()
            crosshair_name = Path(crosshair).name
            crosshair_name_strip = Path(crosshair_name).stem

            shutil.copy2(crosshair, current_dir)
            os.rename(crosshair_name, "hud_bullseye.tga")
            create_crosshair_dir = os.path.join(current_dir, "crosshairs", crosshair_name_strip)
            os.makedirs(create_crosshair_dir, exist_ok=True)
            shutil.copy2(crosshair, create_crosshair_dir) #copy the unmunged crosshair to the crosshair folder to use it for the preview
            subprocess.run(["tools/pc_TextureMunge.exe", "-inputfile", "hud_bullseye.tga", "-platform", "pc", "-outputdir", create_crosshair_dir, "-continue"], creationflags=subprocess.CREATE_NO_WINDOW)
            
            delete_munge_log = "pc_TextureMunge.log"
            delete_tga = "hud_bullseye.tga"
            os.remove(delete_tga)
            os.remove(delete_munge_log)

            root2.destroy()
            crosshair_window()

    def delete_crosshair():

        indices = listbox.curselection()
        lang = listbox.get(indices)
        del_path = os.path.join("crosshairs", lang)
        shutil.rmtree(del_path)

        root2.destroy()
        crosshair_window()

    def switch_to_main_menu():
        root2.destroy()
        main_window()

    def cross_preview():
        indices = listbox.curselection()

        if indices:
            lang = listbox.get(indices)

            preview = tk.Toplevel(root2)
            preview.title("Crosshair Preview")
            preview.attributes('-toolwindow', True)
            ws = preview.winfo_screenwidth()
            hs = preview.winfo_screenheight() 

            x = (ws/3.5)
            y = (hs/5.4)

            preview.resizable(False, False)

            preview.geometry("256x256+%d+%d" % (x,y))

            image_help= lang + ".tga"
            image_path = os.path.join("crosshairs", lang, image_help)

            img = Image.open(image_path)

            resized_img = img.resize((256, 256))

            #make the backround grey and resize it so its not to small in the preview
            if resized_img.mode in ('RGBA', 'LA') or ('transparency' in resized_img.info):
                background = Image.new("RGBA", resized_img.size, (58, 58, 58, 255))
                background.paste(resized_img, (0, 0), resized_img) 
                resized_img = background

            tk_img = ImageTk.PhotoImage(resized_img)
            label = tk.Label(preview, image=tk_img)
            label.image = tk_img
            label.pack(fill="both", expand=True)
        else: return

    apply = tk.Button(root2, text="Apply Crosshair", command=apply_crosshair, bg="#474747", fg="#CACACA", font=("Arial", 16))
    apply.place(relx=0.69, rely=0.8, anchor="center")

    del1 = Button(root2, text="Delete Crosshair", command=delete_crosshair, bg="#474747", fg="#CACACA", font=("Arial", 16))
    del1.place(relx=0.3, rely=0.8, anchor="center")

    swt1 = Button(root2, text= "Main Menu", command= switch_to_main_menu, bg="#474747", fg="#CACACA", font=("Arial", 12))
    swt1.place(relx=0.058, rely=0.03, anchor="center")

    pre = Button(root2, text="Preview", command=cross_preview, bg="#474747", fg="#CACACA", font=("Arial", 16))
    pre.place(relx=0.5, rely=0.801, anchor="center")

    imp1 = Button(root2, text="Import Crosshair", command=lambda:crosshair_import(root2), bg="#474747", fg="#CACACA", font=("Arial", 16))
    imp1.place(relx=0.5, rely=0.2, anchor="center")

    root2.mainloop()

       
def select_file_path(root):
        
        base_game_path = filedialog.askdirectory(title="Select SWBF2 Game Path")
        valid_path = os.path.join(base_game_path, "BattlefrontII.exe")

        if base_game_path and os.path.isfile(valid_path): #checking if the selected folder got a swbf2.exe in it to make sure the user selected the right folder

            os.makedirs("rcs", exist_ok=True)
            os.makedirs("og", exist_ok=True)

            target_game_path = os.path.join(base_game_path, "data", "_lvl_pc",)
            json_game_path = {"game_path" : target_game_path}

            with open(json_path, "w") as f:
                json.dump(json_game_path, f, indent=4)

            back_up_path = os.path.join(target_game_path, "ingame.lvl")
            shutil.copy2(back_up_path, 'og/ingame.lvl')

            root.destroy()          
            main_window()
            
        else: 
            label3 = Label(root, text="Ops that was the wrong folder", font=("Arial", 36), bg="#333333", fg="#ff0000" )
            label3.place(relx=0.5, rely=0.85, anchor="center")


def set_up_window():

    root = tk.Tk()


    root.title("SWBF2 HUD Changer")

    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight() 

    x = (ws/3.5)
    y = (hs/5.4)

    root.resizable(False, False)

    root.geometry("800x600+%d+%d" % (x,y))
    root.configure(bg="#333333")

    label = Label(root, text="SWBF2 HUD Changer", font=("Arial", 36), bg="#333333", fg="#dadada" )
    label.place(relx=0.5, rely=0.1, anchor="center")

    label2 = Label(root, text="Welcome to the SWBF2 HUD Changer :)", font=("Arial", 18), bg="#333333", fg="#dadada")
    label2.place(relx=0.5, rely=0.23,anchor="center")

    label3 = Label(root, text="Please select your GameData folder.\n\nIf you do not know where the GameData folder is go to your Steam/GOG Libary\nand browse for local files. In most cases it is:\n\nC:/steamlibary/steamapps/common/Star Wars Battlefront II Classic/GameData", font=("Arial", 14), bg="#333333", fg="#dadada", justify=LEFT )
    label3.place(relx=0.5, rely=0.45,anchor="center")

    button = Button(root, text="Search", command=lambda:select_file_path(root), width= 15, height=1, font=("Arial", 20), bg="#4D4D4D", fg="#dadada",)
    button.place(relx=0.5, rely=0.7, anchor="center")

    root.mainloop()

#skip setup window if the json file is already there
if os.path.isfile(json_path):
    main_window()
else:
    set_up_window()
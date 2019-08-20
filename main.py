import requests
import locale
import requestCalls
import csv
import json
import datetime
import webbrowser
import xlsxwriter
import tkinter as tk
from tkinter import *
from tkinter.filedialog import *
from tkinter.ttk import *
from tkinter.font import Font
from tkinter import messagebox

products = [] #global list to store product objects
window = Tk() #init main window
locale.setlocale(locale.LC_ALL, '') #set locale
name=StringVar()
desc=StringVar()
price=StringVar()
qty=StringVar()
myFont= Font(family="Times New Roman", size=14) #normal text font
menuFont = Font(family="Times New Roman", size=16) #font for menus
headingFont = Font(family="Times New Roman", size=20, weight="bold") #heading font
v = IntVar() #global variable for radio buttons. see remove or update products
v.set(1) #init IntVar

totalProductsLabel = tk.Label() # init main window labels 
totalUnitsLabel = tk.Label()    # and make them global so they can be updated
totalValueLabel = tk.Label()

def main(): 
    requestProducts()
    gui()


def requestProducts(): #Call api and update products list
    global products
    products=[]
    products = requestCalls.getProducts()
    

def sendProduct(name, desc, price, qty): #Post new product to api
    r=requestCalls.postProduct(name, desc, price, qty)
    requestProducts()
    updateMainLabels()
    return r.status_code


def updateProducts(id,name,description,price,qty): #Put updated product to api
    requestCalls.putProduct(id,name,description,price,qty)
    requestProducts()
    updateMainLabels()


def deleteProduct(id): #delete product from api
    r= requestCalls.deleteProduct(id)
    requestProducts()
    updateMainLabels()

def deleteAllProducts(win):
    response = tk.messagebox.askquestion("Delete All Products", "Are you sure you want to delete all products? \n This action CANNOT be undone!", icon='warning')
    if response == 'yes':
        requestCalls.deleteProducts()
        requestProducts()
        updateMainLabels()
    else:
        return

def gui():
    
    global totalProductsLabel
    global totalUnitsLabel
    global totalValueLabel
    window.title("InvManager")
    window.geometry('800x600')

    rootMenu = Menu(window)
    rootMenu.config(bg="#2f3542")
    window.config(menu=rootMenu,bg="#57606f")
    fileMenu = Menu(rootMenu,tearoff=0)
    fileMenu.config(bg="#2f3542")
    rootMenu.add_cascade(label="File", menu=fileMenu,font=menuFont,activebackground='#596275')
    fileMenu.add_command(label="Import From", command=importFrom,font=menuFont,activebackground='#596275')
    fileMenu.add_command(label="Add Products", command=addProduct,font=menuFont,activebackground='#596275')
    fileMenu.add_command(label="Generate Report", command=report,font=menuFont,activebackground='#596275')
    fileMenu.add_separator()
    fileMenu.add_command(label="Exit", command=rootMenu.quit,font=menuFont,activebackground='#596275')
    
    editMenu = Menu(rootMenu,tearoff=0)
    editMenu.config(bg="#2f3542")
    rootMenu.add_cascade(label="Edit", menu=editMenu,font=menuFont,activebackground='#596275')
    editMenu.add_command(label="Remove Products", command=removeProduct,font=menuFont,activebackground='#596275')
    editMenu.add_command(label="Update Products", command=updateProductGUI,font=menuFont,activebackground='#596275')
    editMenu.add_command(label="Delete All Products", command= lambda win = window : deleteAllProducts(win),font=menuFont,activebackground='#596275')

    frame = tk.Frame(window,bg=window['bg'])
    title=tk.Label(frame,text='InvManager v1.0', font=headingFont,bg=frame['bg'],fg='#f1f2f6')
    title.pack(pady=(50,5))
    totalProducts = len(products)
    totalProductsLabel = tk.Label(frame,text='Total Products: ' + str(f"{totalProducts:,d}"), font=myFont,bg=frame['bg'],fg='#f1f2f6')
    totalProductsLabel.pack(pady=(0,5))
    totalUnitsLabel = tk.Label(frame,text='Total Units: ' + str(totalUnits()), font=myFont,bg=frame['bg'],fg='#f1f2f6')
    totalUnitsLabel.pack(pady=(0,5))
    totalValueLabel = tk.Label(frame,text='Total Value: ' + totalValue(), font=myFont,bg=frame['bg'],fg='#f1f2f6')
    totalValueLabel.pack(pady=(0,5))
    frame.pack(expand=True,fill=BOTH)

    center(window)   

    mainloop()
    
#****** ADD PRODUCTS GUI ******
#******************************
#******************************
def addProduct():

    addProdWindow = Toplevel(window, borderwidth=2, relief = RAISED,bg="#a4b0be")
    addProdWindow.title("Add Product")
    addProdWindow.geometry('500x300')
    addProdWindow.resizable(False, False)
    center(addProdWindow)

    addProdFrame = tk.Frame(addProdWindow)
    addProdFrame.config(bg="#a4b0be")
    addProdFrame.grid_columnconfigure(1, weight=1)

    nameLabel = tk.Label(addProdFrame,text="Product Name:",font=myFont,fg='#2f3542')
    nameLabel.config(bg=addProdFrame['bg'])
    nameLabel.grid(column=0,row=0,sticky=("W"),padx=30, pady=(20,20))

    nameEntry = Entry(addProdFrame,textvariable=name,font=myFont)
    nameEntry.grid(column=1,row=0,sticky=("E","W"),padx=30, pady=(20,20))

    descLabel = tk.Label(addProdFrame,text="Product Description:",font=myFont,fg='#2f3542')
    descLabel.config(bg=addProdFrame['bg'])
    descLabel.grid(column=0,row=1,sticky=("w"),padx=30, pady=(0,20))

    descEntry = Entry(addProdFrame,textvariable=desc,font=myFont)
    descEntry.grid(column=1,row=1,sticky=("E","W"),padx=30, pady=(0,20))

    priceLabel = tk.Label(addProdFrame,text="Product Price:",font=myFont,fg='#2f3542')
    priceLabel.config(bg=addProdFrame['bg'])
    priceLabel.grid(column=0,row=2,sticky=("w"),padx=30, pady=(0,20))
    
    priceEntry = Entry(addProdFrame,textvariable=price,font=myFont)
    priceEntry.grid(column=1,row=2,sticky=("E","W"),padx=30, pady=(0,20))

    qtyLabel = tk.Label(addProdFrame,text="Product Qty:",font=myFont,fg='#2f3542')
    qtyLabel.config(bg=addProdFrame['bg'])
    qtyLabel.grid(column=0,row=3,sticky=("w"),padx=30, pady=(0,20))
    
    qtyEntry = Entry(addProdFrame,textvariable=qty,font=myFont)
    qtyEntry.grid(column=1,row=3,sticky=("E","W"),padx=30, pady=(0,20))

    addProdFrame.pack(expand=True,fill=BOTH)
    cancelButton = Button(addProdWindow, text='Quit', command= lambda win = addProdWindow : quit(win))
    cancelButton.pack(side=RIGHT,pady=(30),padx=(0,20),anchor=S)

    submitButton = Button(addProdWindow, text='Submit', command= lambda name=nameEntry,desc=descEntry,price=priceEntry,qty=qtyEntry,window=addProdWindow : submit(name,desc,price,qty,window))
    submitButton.pack(side=RIGHT,pady=(30),padx=(10),anchor=S)

def submit(name,desc,price,qty,window):
    prodname = name.get()
    prodDesc = desc.get()
    prodPrice = price.get()
    prodQty = qty.get()
    
    if prodname != "" and prodDesc != "" and prodPrice != "" and prodQty != "" :
        s=sendProduct(prodname,prodDesc,float(prodPrice),int(prodQty))
        if s == 200:
            messagebox.showinfo("Success","Product "+prodname+" was added successfully!",parent=window)
            name.delete(0, END)
            desc.delete(0, END)
            price.delete(0, END)
            qty.delete(0, END)
        else:
            messagebox.showerror("Error","Looks like something went wrong. Please try again.",parent=window)
    else:
        messagebox.showerror("Error","All fields are required. Make sure each field has a value.",parent=window)
 

#****** REMOVE PRODUCTS GUI ******
#*********************************
#*********************************
def removeProduct():

    removeProdWindow = Toplevel(window, borderwidth=2, relief = RAISED)
    removeProdWindow.config(bg="#a4b0be")
    removeProdWindow.title("Remove Product")
    removeProdWindow.geometry('500x200')
    removeProdWindow.resizable(False, False)
    center(removeProdWindow)
    

    searchProdFrame = tk.Frame(removeProdWindow)
    searchProdFrame.config(bg="#a4b0be")
    searchProdFrame.grid_columnconfigure(1, weight=1)

    searchLabel = tk.Label(searchProdFrame,text="Search by ID or Name:",font=myFont,fg='#2f3542')
    searchLabel.config(bg=searchProdFrame['bg'])
    searchLabel.grid(column=0,row=0,sticky=("E","W"),padx=30, pady=(20,20))

    searchEntry = Entry(searchProdFrame,textvariable=name,font=myFont)
    searchEntry.grid(column=1,row=0,sticky=("E","W"),padx=30, pady=(20,20))
    searchEntry.delete(0,END)

    searchProdFrame.pack(expand=True,fill=BOTH)
    cancelButton = Button(removeProdWindow, text='Cancel', command= lambda win = removeProdWindow : quit(win))
    cancelButton.pack(side=RIGHT,pady=(30),padx=(0,20),anchor=S)
    submitButton = Button(removeProdWindow, text='Submit', command= lambda name=searchEntry, win=removeProdWindow, frame=searchProdFrame : searchProd(name,win,frame))
    submitButton.pack(side=RIGHT,pady=(30),padx=(10),anchor=S)


#****** UPDATE PRODUCTS GUI ******
#*********************************
#*********************************
def updateProductGUI():

    updateProdWindow = Toplevel(window, borderwidth=2, relief = RAISED)
    updateProdWindow.config(bg="#a4b0be")
    updateProdWindow.title("Update Product")
    updateProdWindow.geometry('500x200')
    updateProdWindow.resizable(False, False)
    center(updateProdWindow)
    

    searchProdFrame = tk.Frame(updateProdWindow)
    searchProdFrame.config(bg="#a4b0be")
    searchProdFrame.grid_columnconfigure(1, weight=1)

    searchLabel = tk.Label(searchProdFrame,text="Search by ID or Name:",font=myFont,fg='#2f3542')
    searchLabel.config(bg=searchProdFrame['bg'])
    searchLabel.grid(column=0,row=0,sticky=("E","W"),padx=30, pady=(20,20))

    searchEntry = Entry(searchProdFrame,textvariable=name,font=myFont)
    searchEntry.grid(column=1,row=0,sticky=("E","W"),padx=30, pady=(20,20))
    searchEntry.delete(0,END)

    searchProdFrame.pack(expand=True,fill=BOTH)
    cancelButton = Button(updateProdWindow, text='Cancel', command= lambda win = updateProdWindow : quit(win))
    cancelButton.pack(side=RIGHT,pady=(30),padx=(0,20),anchor=S)
    submitButton = Button(updateProdWindow, text='Submit', command= lambda name=searchEntry, win=updateProdWindow, frame=searchProdFrame : searchProd(name,win,frame))
    submitButton.pack(side=RIGHT,pady=(30),padx=(10),anchor=S)

def updateInfo(win):
    id=v.get()
    name = ""
    desc = ""
    price = 0.0 
    qty = 0
    for i in products:
        if i.id == id:
            name=i.name
            desc=i.description
            price=i.price
            qty=i.qty

    for child in win.winfo_children():
        child.destroy()
    
    updateProdFrame = tk.Frame(win)
    updateProdFrame.config(bg="#a4b0be")
    updateProdFrame.grid_columnconfigure(1, weight=1)

    nameLabel = tk.Label(updateProdFrame,text="Product Name:",font=myFont,fg='#2f3542')
    nameLabel.config(bg=updateProdFrame['bg'])
    nameLabel.grid(column=0,row=0,sticky=("W"),padx=30, pady=(20,20))

    nameEntry = Entry(updateProdFrame,textvariable=name,font=myFont)
    nameEntry.grid(column=1,row=0,sticky=("E","W"),padx=30, pady=(20,20))
    nameEntry.delete(0,END)
    nameEntry.insert(0,name)


    descLabel = tk.Label(updateProdFrame,text="Product Description:",font=myFont,fg='#2f3542')
    descLabel.config(bg=updateProdFrame['bg'])
    descLabel.grid(column=0,row=1,sticky=("w"),padx=30, pady=(0,20))

    descEntry = Entry(updateProdFrame,textvariable=desc,font=myFont)
    descEntry.grid(column=1,row=1,sticky=("E","W"),padx=30, pady=(0,20))
    descEntry.delete(0,END)
    descEntry.insert(0,desc)

    priceLabel = tk.Label(updateProdFrame,text="Product Price:",font=myFont,fg='#2f3542')
    priceLabel.config(bg=updateProdFrame['bg'])
    priceLabel.grid(column=0,row=2,sticky=("w"),padx=30, pady=(0,20))
    
    priceEntry = Entry(updateProdFrame,textvariable=price,font=myFont)
    priceEntry.grid(column=1,row=2,sticky=("E","W"),padx=30, pady=(0,20))
    priceEntry.delete(0,END)
    priceEntry.insert(0,str(price))

    qtyLabel = tk.Label(updateProdFrame,text="Product Qty:",font=myFont,fg='#2f3542')
    qtyLabel.config(bg=updateProdFrame['bg'])
    qtyLabel.grid(column=0,row=3,sticky=("w"),padx=30, pady=(0,20))
    
    qtyEntry = Entry(updateProdFrame,textvariable=qty,font=myFont)
    qtyEntry.grid(column=1,row=3,sticky=("E","W"),padx=30, pady=(0,20))
    qtyEntry.delete(0,END)
    qtyEntry.insert(0,str(qty))

    updateProdFrame.pack(expand=True,fill=BOTH)
    cancelButton = Button(win, text='Quit', command= lambda win = win : quit(win))
    cancelButton.pack(side=RIGHT,pady=(30),padx=(0,20),anchor=S)


    submitButton = Button(win, text='Submit', command= lambda name=nameEntry,desc=descEntry,price=priceEntry,qty=qtyEntry,window=win : updateProduct(name,desc,price,qty,window))
    submitButton.pack(side=RIGHT,pady=(30),padx=(10),anchor=S)


#****** SEARCH PRODUCT GUI ******
#********************************
#********************************
def searchProd(name,win,frame):
    s = name.get()
    requestProducts()
    matches=[]
    for i in products:
        try:
            if int(i.id) == int(s) or s in i.name:
                matches.append([str(i.id),i.name,i.description,str(i.price),str(i.qty)])
        except ValueError as e:
            if s in i.name:
                matches.append([str(i.id),i.name,i.description,str(i.price),str(i.qty)])
    showProd(matches,win,frame)
        

def showProd(matches,win,frame):
    if win.title() == "Remove Product":
        for child in win.winfo_children():
            child.destroy()
        win.geometry('500x450')
        win.resizable(True, True)
        win.minsize(500,450)
        count = 0
        name = 'prod ' + str(count)
        text = ""
        frame.destroy()
        canvas = Canvas(win,bg="#a4b0be",highlightthickness=0)
        scrollbary = Scrollbar(win,orient=VERTICAL,command = canvas.yview)
        scrollbarx = Scrollbar(win,orient=HORIZONTAL,command = canvas.xview)
        scrollbarx.pack( side = BOTTOM, fill = X)
        scrollbary.pack( side = RIGHT, fill = Y )
        canvas.pack(anchor='w',expand=True,fill=BOTH)
        canvas.configure(yscrollcommand = scrollbary.set,xscrollcommand=scrollbarx.set)
        showProdFrame = tk.Frame(canvas)
        showProdFrame.config(bg="#a4b0be")
        canvas.create_window((0,0), window=showProdFrame, anchor='nw')
        l = tk.Label(showProdFrame,text='Select a product to delete',font=Font(family="Times New Roman", size=16),bg=showProdFrame['bg'],fg='#2f3542')
        l.pack(anchor='nw',pady=(5),padx=(5))
        for i in matches:
            text = "ID: " + i[0] + " | " + "Name: " + i[1] + " | " + "Desc: " +  i[2] + " | " + "Price: " + i[3] + " | " + "Qty: " + i[4] 
            val = int(i[0])
            a = tk.Radiobutton(showProdFrame, text=text, variable=v, value=i[0],bg=showProdFrame['bg'],fg='#2f3542')
            a.pack(anchor='w',pady=(5),padx=(5))
            count+=1
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'))
        cancelButton = Button(win, text='Cancel', command= lambda win = win : quit(win))
        cancelButton.pack(side=RIGHT,pady=(30),padx=(0,20),anchor=S)
        submitButton = Button(win, text='Submit', command= lambda win = win : delete(win))
        submitButton.pack(side=RIGHT,pady=(30),padx=(10),anchor=S)

    elif win.title() == "Update Product":
        for child in win.winfo_children():
            child.destroy()
        win.geometry('500x450')
        count = 0
        name = 'prod ' + str(count)
        text = ""
        frame.destroy()
        canvas = Canvas(win,bg="#a4b0be",highlightthickness=0)
        scrollbary = Scrollbar(win,orient=VERTICAL,command = canvas.yview)
        scrollbarx = Scrollbar(win,orient=HORIZONTAL,command = canvas.xview)
        scrollbarx.pack( side = BOTTOM, fill = X)
        scrollbary.pack( side = RIGHT, fill = Y )
        canvas.pack(anchor='w',expand=True,fill=BOTH)
        canvas.configure(yscrollcommand = scrollbary.set,xscrollcommand=scrollbarx.set)
        showProdFrame = tk.Frame(canvas)
        showProdFrame.config(bg="#a4b0be")
        canvas.create_window((0,0), window=showProdFrame, anchor='nw')
        l = tk.Label(showProdFrame,text='Select a product to update',font=Font(family="Times New Roman", size=16),bg=showProdFrame['bg'],fg='#2f3542')
        l.pack(anchor='nw',pady=(5),padx=(5))
        for i in matches:
            text = "ID: " + i[0] + " | " + "Name: " + i[1] + " | " + "Desc: " +  i[2] + " | " + "Price: " + i[3] + " | " + "Qty: " + i[4] 
            val = int(i[0])
            a = tk.Radiobutton(showProdFrame, text=text, variable=v, value=i[0],bg=showProdFrame['bg'],fg='#2f3542')
            a.pack(anchor='w',pady=(5),padx=(5))
            count+=1
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'))
        cancelButton = Button(win, text='Cancel', command= lambda win = win : quit(win))
        cancelButton.pack(side=RIGHT,pady=(30),padx=(0,20),anchor=S)
        submitButton = Button(win, text='Submit', command= lambda win = win : updateInfo(win))
        submitButton.pack(side=RIGHT,pady=(30),padx=(10),anchor=S)


#****** IMPORT FROM ******
#*************************
#*************************
def importFrom ():
    filename = askopenfilename()
    jsonPath = 'products.json'
    arr=[]

    with open (filename) as csvFile:
        csvReader = csv.DictReader(csvFile)
        for csvRow in csvReader:
            arr.append(csvRow)

    with open(jsonPath, "w") as jsonFile:
        jsonFile.write(json.dumps(arr, indent = 4))
    
    requestCalls.postCSV()
    requestProducts()


#****** GENERATE REPORT ******
#*****************************
#*****************************
def report():
    requestProducts()
    data = []
    total = 1
    workbook = xlsxwriter.Workbook('InventoryReport.xlsx')
    worksheet = workbook.add_worksheet()
    for i in products:
        data.append([str(i.id),i.name,i.description,str(i.price), str(i.qty)])
        total += 1

    
    options = {'data': data,
    'style': 'Table Style Medium 2',
    'columns': [{'header': 'ID'},
                {'header': 'Name'},
                {'header': 'Desc'},
                {'header': 'Price'},
                {'header': 'Qty'}
                ]}
    worksheet.add_table('B1:F'+str(total), options)
    workbook.close()
    webbrowser.open('InventoryReport.xlsx',new=1, autoraise=True)

#****** General Functions ******
#*******************************
#*******************************

def totalValue():
    totalvalue = 0
    for i in products:
        totalvalue += (float(i.qty) * float(i.price))
    
    ret= locale.currency(totalvalue, grouping=True)  
    return ret 

def totalUnits():
    totalunits = 0
    for i in products:
        totalunits += int(i.qty)

    return f"{totalunits:,d}"    

def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def delete(win):
    id = v.get()
    deleteProduct(id)
    win.destroy()
    removeProduct()

def updateMainLabels():
    global totalProductsLabel
    global totalUnitsLabel
    global totalValueLabel
    totalProducts = len(products)
    totalProductsLabel.config(text='Total Products: ' + str(f"{totalProducts:,d}"))
    totalUnitsLabel.config(text='Total Units: ' + str(totalUnits()))
    totalValueLabel.config(text='Total Value: ' + totalValue())


def updateProduct(name,desc,price,qty,win):
    id=v.get()
    prodname=name.get()
    prodDesc=desc.get()
    prodPrice=price.get()
    prodQty=qty.get()

    updateProducts(id,prodname,prodDesc,prodPrice,prodQty)

    name.delete(0, END)
    desc.delete(0, END)
    price.delete(0, END)
    qty.delete(0, END)

    win.destroy()
    updateProductGUI()

def quit(win):
    win.destroy()


if __name__ == "__main__":
    main()
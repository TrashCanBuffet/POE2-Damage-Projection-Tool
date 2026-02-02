#########################################################################################
#
# damage_equation.py
#
#########################################################################################
#
# Built using:
#   Python (3.13.1)
#   (Program doesn't use any crazy features, so should work on older versions... possibly)
#
#########################################################################################
#
# Purpose:
#   To assist with damage annalysis in Path of Exile II using linear algebra and
# partial derivatives
#
# Intended opperation:
#   This script is intended to be ran through the Python IDLE Shell.
#   While it could be ran through a system python command call of the script with the
# interactive paramiter '-i', I wanted to keep it as a single script file that didn't require
# a batch file packaged with it or required to be ran through the system terminal.
#
#########################################################################################

#Global lists of damage types as strings
DTYPES = ["p","f","o","l","c"]

#Declare gobal identity vector (used in 1 (+) inc and 1 (+) more)
ONE = None

#Declaring global instances of damage lists and matrices (redefined later in conctruct functions)
base=added=conv1=extra1=conv2=extra2=inc=more = None

#Valid variables
validList=[]

#Table used to hold derivatives for sorting
derivTable={}
#Need a table that has the position in terms of value
orderTable={}

#Dictionary of user functions and a description of their use.
funcDict={
        "p_deriv(variable)":"Not necessary to call for getting the numeric values of the partial derivatives, but can be used to get the stringified variable representation of the partial derivative.[Note: this will not print the vector, but returns a vector]",
        "mix_p_deriv(variable1,variable2)":"This function isn't called by the script, but is a left over from me fiddling around with stuff and testing.",
        "print_mat(mat)":"Prints the matrix.",
        "print_vect(vect)":"Prints the vector.",
        "print_value_data()":"Prints every vector/matrix for calculating damage, but with the variables currently set value.",
        "all_dmg()":"Prints the partial derivative of damage with respect to each variable in descending order of damage change magnitude.",
        "dmg()":"Prints the total damage with the variables currently set value."
    }

#Used to populate base and added
def create_vect(arrType):
    arr= ["" for _ in range(5)]
    for i in range(5):
        arr[i]=DTYPES[i]+"_"+arrType
        validList.append(arr[i])
    return arr

#Used to populate conv1,extra1,and conv2
def create_mat(matType):
    mat= [["" for _ in range(5)] for _ in range(5)]
    for i in range(5):
        for j in range(5):
            mat[i][j] = DTYPES[i]+DTYPES[j]+"_"+matType
            validList.append(mat[i][j])
    return mat

#Used to populate ONE
def create_id_mat():
    mat= [["0.0" for _ in range(5)] for _ in range(5)]
    for i in range(5):
        for j in range(5):
            if j == i:
                mat[i][j] = "1"
    return mat

#Used to populate inc and more
def create_type_id_mat(matType):
    mat= [["0.0" for _ in range(5)] for _ in range(5)]
    for i in range(5):
        for j in range(5):
            if j == i:
                mat[i][j] = DTYPES[i]+"_"+matType
                validList.append(mat[i][j])
    return mat

#Create global variables for damage
def create_globals():
    for v in validList:
        compart = v.split("_")
        if "conv" in compart[1] and compart[0][0] == compart[0][1]:
            globals()[v] = 1.0
        else:
            globals()[v] = 0.0

#Vector addition
def add_vect(vect1,vect2):
    arr= ["" for _ in range(5)]
    for i in range(5):
        if vect1[i] == "0.0":
            arr[i] = vect2[i]
        elif vect2[i] == "0.0":
            arr[i] = vect1[i]
        else:
            arr[i] = vect1[i]+"+"+vect2[i]
    return arr

#Matrix addition
def add_mat(mat1,mat2):
    mat= [["" for _ in range(5)] for _ in range(5)]
    for i in range(5):
        for j in range(5):
            if mat1[i][j] == "0.0":
                mat[i][j] = mat2[i][j]
            elif mat2[i][j] == "0.0":
                mat[i][j] = mat1[i][j]
            else:    
                mat[i][j] = mat1[i][j]+"+"+mat2[i][j]
    return mat

#Dot product of vector by matrix; product is a vector
def mult_vect_mat(vect,mat):
    arr= ["" for _ in range(5)]
    for i in range(5):
        for j in range(5):
            if vect[j] == "0.0" or mat[j][i] == "0.0" or vect[j] == "":
                continue
            elif vect[j] == "1":
                arr[i] = arr[i]+"("+mat[j][i]+")+\n"
            elif mat[j][i] == "1":
                arr[i] = arr[i]+"("+vect[j]+")+\n"
            else:
                arr[i] = arr[i]+"("+vect[j]+")*("+mat[j][i]+")+\n"
        arr[i] = arr[i][:-2]

    #Looking for empty cells and placing a '0'
    for a in range(5):
        if arr[a] == "":
            arr[a] = "0.0"

    return arr

#   Yes, in general practice it is bad to have variable names the same as globals,
#but I am not renaming and rewriting what I typed for testing my functions, you can't make me.
#   I added the parameters so I can feed the vector,matrix after partial derivation without changing the
#original global variables.
def cal_damage(base,added,conv1,extra1,conv2,extra2,inc,more,one1,one2):
    return  mult_vect_mat(
                mult_vect_mat(
                    mult_vect_mat(
                        mult_vect_mat(
                            add_vect(base,added),
                            add_mat(conv1,extra1)),
                        add_mat(conv2,extra2)),
                    add_mat(one1,inc)),
                add_mat(one2,more))

#   Applies values to damage variables.
def damage_val(dmg):
    dmg_val = [0 for _ in range(5)]
    dmg = replace_veriable(dmg)
    for i in range(5):
        dmg_val[i] = eval(dmg[i])
    return dmg_val

#   Have to replace variables with their value manually...
def replace_veriable(dmg):
    for i in range(5):
        if dmg[i] == "0.0":
            continue
        for v in validList:
            if v in dmg[i]:
                dmg[i]= dmg[i].replace(v,str(globals()[v]))
    return dmg
        
#   Creates the vector resulting from a derivative with respects to a variable held within said vector.
def deriv_vect(i):
    newVect= ["0.0" for _ in range(5)]
    newVect[i]="1"
    return newVect
    
#   Creates the matrix resulting from a derivative with respects to a variable held within said matrix.
def deriv_mat(i,j):
    newMat= [["0.0" for _ in range(5)] for _ in range(5)]
    newMat[i][j]="1"
    return newMat

#   Take the partial derivative with respects to a given the string name of the variable
def p_deriv(variable):
    #   Valid input check
    if not variable in validList:
        print("invalid variable field")
        return
    
    compart= variable.split("_")
    
    newBase = base
    newAdded = added
    newConv1 = conv1
    newExtra1 = extra1
    newConv2 = conv2
    newExtra2 = extra2
    newInc = inc
    newMore = more
    newOne1 = ONE
    newOne2 = ONE
    d_type = list(compart[0])
    
    match compart[1]:
        case "base":
            newBase = deriv_vect(DTYPES.index(d_type[0]))
            newAdded = ["0.0" for _ in range(5)]
        case "added":
            newAdded = deriv_vect(DTYPES.index(d_type[0]))
            newBase = ["0.0" for _ in range(5)]
        case "conv1":
            newConv1 = deriv_mat(DTYPES.index(d_type[0]),DTYPES.index(d_type[1]))
            newExtra1 = [["0.0" for _ in range(5)] for _ in range(5)]
        case "extra1":
            newExtra1 = deriv_mat(DTYPES.index(d_type[0]),DTYPES.index(d_type[1]))
            newConv1 = [["0.0" for _ in range(5)] for _ in range(5)]
        case "conv2":
            newConv2 = deriv_mat(DTYPES.index(d_type[0]),DTYPES.index(d_type[1]))
            newExtra2 = [["0.0" for _ in range(5)] for _ in range(5)]
        case "extra2":
            newExtra2 = deriv_mat(DTYPES.index(d_type[0]),DTYPES.index(d_type[1]))
            newConv2 = [["0.0" for _ in range(5)] for _ in range(5)]
        case "inc":
            newInc = deriv_mat(DTYPES.index(d_type[0]),DTYPES.index(d_type[0]))
            newOne1 = [["0.0" for _ in range(5)] for _ in range(5)]
        case "more":
            newMore = deriv_mat(DTYPES.index(d_type[0]),DTYPES.index(d_type[0]))
            newOne2 = [["0.0" for _ in range(5)] for _ in range(5)]
        case _:
            pass

    return cal_damage(newBase, newAdded, newConv1, newExtra1, newConv2, newExtra2, newInc, newMore, newOne1, newOne2)

#   Take the mix partial derivative with respects to the given string names of two variables.
#Note: Not used or called in program.
def mix_p_deriv(variable1,variable2):
    if not (variable1 in validList and variable2 in validList):
        return "0.0"

    compart1= variable1.split("_")
    compart2= variable2.split("_")
    
    newBase = base
    newAdded = added
    newConv1 = conv1
    newExtra1 = extra1
    newConv2 = conv2
    newExtra2 = extra2
    newInc = inc
    newMore = more
    newOne1 = ONE
    newOne2 = ONE
    d_type1 = list(compart1[0])
    d_type2 = list(compart2[0])

    match compart1[1]:
        case "base":
            newBase = deriv_vect(DTYPES.index(d_type1[0]))
            newAdded = ["0.0" for _ in range(5)]
        case "added":
            newAdded = deriv_vect(DTYPES.index(d_type1[0]))
            newBase = ["0.0" for _ in range(5)]
        case "conv1":
            newConv1 = deriv_mat(DTYPES.index(d_type1[0]),DTYPES.index(d_type1[1]))
            newExtra1 = [["0.0" for _ in range(5)] for _ in range(5)]
        case "extra1":
            newExtra1 = deriv_mat(DTYPES.index(d_type1[0]),DTYPES.index(d_type1[1]))
            newConv1 = [["0.0" for _ in range(5)] for _ in range(5)]
        case "conv2":
            newConv2 = deriv_mat(DTYPES.index(d_type1[0]),DTYPES.index(d_type1[1]))
            newExtra2 = [["0.0" for _ in range(5)] for _ in range(5)]
        case "extra2":
            newExtra2 = deriv_mat(DTYPES.index(d_type1[0]),DTYPES.index(d_type1[1]))
            newConv2 = [["0.0" for _ in range(5)] for _ in range(5)]
        case "inc":
            newInc = deriv_mat(DTYPES.index(d_type1[0]),DTYPES.index(d_type1[0]))
            newOne1 = [["0.0" for _ in range(5)] for _ in range(5)]
        case "more":
            newMore = deriv_mat(DTYPES.index(d_type1[0]),DTYPES.index(d_type1[0]))
            newOne2 = [["0.0" for _ in range(5)] for _ in range(5)]
        case _:
            pass

    #   I feel like this can be done recurssively,
    #but since these are as a string I have to manually consider
    #the previous cases with how I have implemented it currently.
    #ie->probably a better way to do this which would allow
    match compart2[1]:
        case "base":
            if compart1[1] != "added":
                newBase = deriv_vect(DTYPES.index(d_type2[0]))
            newAdded = ["0.0" for _ in range(5)]
            if compart1[1] == "base":
                #This is just to save time and not itterate a new matrix of "0.0"'s
                newBase = newAdded
        case "added":
            if compart1[1] != "base":
                newAdded = deriv_vect(DTYPES.index(d_type2[0]))
            newBase = ["0.0" for _ in range(5)]
            if compart1[1] == "added":
                newAdded = newBase
        case "conv1":
            if compart1[1] != "extra1":
                newConv1 = deriv_mat(DTYPES.index(d_type2[0]),DTYPES.index(d_type2[1]))
            newExtra1 = [["0.0" for _ in range(5)] for _ in range(5)]
            if compart1[1] == "conv1":
                newConv1 = newExtra1
        case "extra1":
            if compart1[1] != "conv1":
                newExtra1 = deriv_mat(DTYPES.index(d_type2[0]),DTYPES.index(d_type2[1]))
            newConv1 = [["0.0" for _ in range(5)] for _ in range(5)]
            if compart1[1] == "extra1":
                newExtra1 = newConv1
        case "conv2":
            if compart1[1] != "extra2":
                newConv2 = deriv_mat(DTYPES.index(d_type2[0]),DTYPES.index(d_type2[1]))
            newExtra2 = [["0.0" for _ in range(5)] for _ in range(5)]
            if compart1[1] == "conv2":
                newConv2 = newExtra2
        case "extra2":
            if compart1[1] != "conv2":
                newExtra2 = deriv_mat(DTYPES.index(d_type2[0]),DTYPES.index(d_type2[1]))
            newConv2 = [["0.0" for _ in range(5)] for _ in range(5)]
            if compart1[1] == "extra2":
                newExtra2 = newConv2
        case "inc":
            newInc = deriv_mat(DTYPES.index(d_type2[0]),DTYPES.index(d_type2[0]))
            newOne1 = [["0.0" for _ in range(5)] for _ in range(5)]
        case "more":
            newMore = deriv_mat(DTYPES.index(d_type2[0]),DTYPES.index(d_type2[0]))
            newOne2 = [["0.0" for _ in range(5)] for _ in range(5)]
        case _:
            pass
    
    return cal_damage(newBase, newAdded, newConv1, newExtra1, newConv2, newExtra2, newInc, newMore, newOne1, newOne2)
        
#   Used to print a matrix into a more readable format
def print_mat(mat):
    for vect in mat:
        print_vect(vect)

#   Used to print a vector into a more readable format
#(mainly for the vectors with longer elements like the end damage)
#[Edit: no longer using program to show only stringified variable results.
#Making script more useful for damage analysis. So it's sort of redundent to use this,
#but i'll keep it because I don't want to go through and rewrite stuff]
def print_vect(vect):
    #redundent, but helps user know that it's printing a vector... i guess...
    print(vect)

#   Used to print the matrix with all entries replaced with the corresponding value of the variable given the string name.
def print_value_mat(mat):
    valMat= [[0.0 for _ in range(5)]for _ in range(5)]
    for i in range(5):
        for j in range(5):
            valMat[i][j]=eval(mat[i][j])
    print_mat(valMat)

#   Used to print the vector with all entries replaced with the corresponding value of the variable given the string name.
def print_value_vect(vect):
    valVect= [0.0 for _ in range(5)]
    for i in range(5):
        valVect[i] = eval(vect[i])
    print_vect(valVect)

#   Used to print every damage matrix/vector with their currently assigned numeric value.
def print_value_data():
    # Yeah... I'm going to hard-code this... it's going to be disgusting...
    print("base:")
    print_value_vect(base)
    print("added:")
    print_value_vect(added)
    print("conv1:")
    print_value_mat(conv1)
    print("extra1:")
    print_value_mat(extra1)
    print("conv2:")
    print_value_mat(conv2)
    print("extra2:")
    print_value_mat(extra2)
    print("inc:")
    print_value_mat(inc)
    print("more:")
    print_value_mat(more)
            

#   Redefine globals with constructed string vectors/matrices
def init_globals():
    global ONE
    ONE = create_id_mat()
    
    global base
    base = create_vect("base")

    global added
    added = create_vect("added")

    global conv1
    conv1 = create_mat("conv1")
    
    global extra1
    extra1 = create_mat("extra1")
    
    global conv2
    conv2 = create_mat("conv2")

    global extra2
    extra2 = create_mat("extra2")

    #   Yes it would be faster program-wise to treat inc and more as a "diagonal" vector and not bother with the "0.0" cases,
    #but adding the "0.0" case handling helps with consolidating all calculations including those for partial derivatives to a singular function,
    #so I did this... deal wid'it.

    global inc
    inc = create_type_id_mat("inc")

    global more
    more = create_type_id_mat("more")

    create_globals()

#   Prints initial information for user about the program.
def dmg_help():
    print("p=physical\tf=fire\to=cold\tl=lightning\tc=chaos")
    print("Damage fields are in the respective order as displayed above^")
    print("rows denote \"source\" damage type, columns denote \"destination\" damage type.\n")
    print("Before you begin calculations, input the values you have.\nValid variables:")
    output=""
    for v in validList:
        output=output+f"{v}\t"
    print(output)
    print("After you have set the necessary values, call function \"all_dmg()\". This will calculate all the partial derivatives for each variable.")
    print("For a list of relevent functions and their description, call function \"func_help()\".\n")

#   Prints the list of functions intended for the user to use along with a description of their use reletive to the use as a user.
def func_help():
    for func, desc in funcDict.items():
        print(f"{func}:\t{desc}\n")

#   Calculates the damage given the damage values and prints the result.
def dmg():
    damage= cal_damage(base,added,conv1,extra1,conv2,extra2,inc,more,ONE,ONE)
    valDamage= damage_val(damage)
    print("Damage:")
    print_vect(valDamage)

#   Calculates every partial derivative with respect to every variable and prints the result.
def all_dmg():
    global derivTable
    global orderTable
    for v in validList:
        dmg= p_deriv(v)
        valDmg= damage_val(dmg)
        derivTable[v]=valDmg
        orderTable[v]=sum(valDmg)
    orderTable= sort_table(orderTable)
    for key in list(orderTable):
        if orderTable[key] != 0:
            print(f"p_deriv({key}):")
            print_vect(derivTable[key])

#   Sorts the dictionary of variables based on the sum of the vector elements.
#This is so the most relevent data to the user is at the top of the print. 
def sort_table(table):
    return dict(sorted(table.items(), key=lambda item: item[1], reverse=True))

#####################################################
#   Program function calls
#####################################################
    
#   Initialize globals
init_globals()
dmg_help()


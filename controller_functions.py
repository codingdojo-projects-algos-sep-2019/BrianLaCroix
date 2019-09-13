from flask import render_template, request, redirect
from config import db
from models import *
import re

###################
#
# General tools, used throughout the application

def consoleMsg(msg):
    ''' This function is intended to be used at the beginning of the execution of each router, to make debugging much easier
    by including 80 asterisks in the beginning to help the eye easily identify the beginning of said function.
    '''
    print('*'*80)
    print(msg)

def linecard_list(router_id):
    ''' Accepts an integer that matches with the 'routers' table, 'id' column.  Queries the DB for all info on this router, 
    then parses the router.linecards_installed field, building a list where the index of the list is the router slot number.

    EXAMPLE:  
    In the following list, there are four dictionaries representing the four linecard slots in a router.  In this example, 
    there is NO linecard in slots 0, 2, 3; there is one linecard in slot 1, with a linecard_type_id of 2 and a router_linecard_id
    value of 8:
    linecard_list = [ {}, {'linecard_type_id': 2, 'router_linecard_id': 8}, {}, {} ]
    '''
    # Get current router + current router's installed linecards
    router = routers.query.get(router_id)

    # Build out a blank list-of-dictionaries structure for the current router, based on number of linecard slots available
    linecard_list=[]
    for i in range(router.router_type.num_slots+10):    
        # added 10 to num_slots; if a router were downsized, it may still have router linecards in the db.  it would be more
        # graceful to delete linecards table entries for cards that don't have slots when changing router_type field,
        # but this is a class project and doesn't have to be perfect, this is quicker, so that's what I'm doing.  :)
        linecard_list.append({})
    
    # Iterate through current linecards, updating the dict entry for the linecard based on it's index
    for linecard in router.linecards_installed:
        linecard_list[linecard.router_slot]={
            'linecard_type_id': linecard.linecard_type_id,
            'router_linecard_id': linecard.id,
            'num_ports': linecard.linecard_type.num_ports,
            'sql_data': linecard,
            'interfaces': []
        }

        # create a list of dictionaries for tracking interfaces by port number
        for i in range(linecard.linecard_type.num_ports):
            linecard_list[linecard.router_slot]['interfaces'].append({})

        # Stuff interfaces into the correct port offset
        for interface in linecard.interfaces_installed:
            print ("interface data =",interface.linecard_port_num,interface.comment,interface.ip_address_v4)
            linecard_list[linecard.router_slot]['interfaces'][int(interface.linecard_port_num)]['interface_id']=interface.id
            # linecard_list[linecard.router_slot]['interfaces'][int(interface.linecard_port_num)]['port']=interface.linecard_port_num
            linecard_list[linecard.router_slot]['interfaces'][int(interface.linecard_port_num)]['comment']=interface.comment
            linecard_list[linecard.router_slot]['interfaces'][int(interface.linecard_port_num)]['ip_address']=interface.ip_address_v4



    # print and return results
    print (linecard_list)
    return linecard_list

###################
#
# Main page stuffs

def index():
    consoleMsg('User landed on home page')
    data=routers.query.all()
    print ("Router list:",data)
    return render_template("index.html", routers=data)

def router_search():
    consoleMsg('User doing search query')
    q=request.form['search_data']+"%%"
    data=routers.query.filter(routers.name.like(q))
    rtr_types=router_types.query.all()
    print ("Router list:",data)
    return render_template("partial/router_index.html", routers=data,rtr_types=rtr_types)



###################
#
#   THE FOLLOWING SECTION IS FOR CREATING AND DELETING OF ROUTER_TYPES

def router_types_index():
    consoleMsg('User requested to go to router_type index page')
    data=router_types.query.all()
    print(data)
    return render_template("partial/router_types_index.html", router_types=data)

def router_type_add():
    consoleMsg('User requested to add router_type')
    data = router_types(
        model=request.form['model'],
        num_slots=request.form['num_slots']
    )
    print (data)
    db.session.add(data)
    db.session.commit()
    data=router_types.query.all()
    print(data)
    return render_template("partial/router_types_index.html", router_types=data)
     
def router_type_delete(router_type_id):
    consoleMsg('User requested to delete router_type with id of'+str(router_type_id))
    # Delete router_type
    data = router_types.query.get(router_type_id)
    db.session.delete(data)
    db.session.commit()
    # Get updated router_type list
    data=router_types.query.all()
    print(data)
    return render_template("partial/router_types_index.html", router_types=data)

###################
#
#   THE FOLLOWING SECTION IS FOR CREATING AND DELETING OF LINECARD TYPES

def linecard_types_index():
    consoleMsg('User requested to go to linecard type index page')
    data=linecard_types.query.all()
    print(data)
    return render_template("partial/linecard_types_index.html", linecard_types=data)

def linecard_type_add():
    consoleMsg('User requested to add linecard_type')
    data = linecard_types(
        model=request.form['model'],
        num_ports=request.form['num_ports'],
        description=request.form['description']
    )
    print (data)
    db.session.add(data)
    db.session.commit()
    data=linecard_types.query.all()
    print(data)
    return render_template("partial/linecard_types_index.html", linecard_types=data)

def linecard_type_delete(linecard_type_id):
    consoleMsg('User requested to delete linecard_type with id of'+str(linecard_type_id))
    # Delete linecard_type_id
    data = linecard_types.query.get(linecard_type_id)
    db.session.delete(data)
    db.session.commit()
    # Get updated linecard_type list
    data=linecard_types.query.all()
    print(data)
    return render_template("partial/linecard_types_index.html", linecard_types=data)

###################
#
#   THE FOLLOWING SECTION IS FOR CREATING AND DELETING OF INTERFACE_TYPES

def interface_types_index():
    consoleMsg('User requested to go to router_type index page')
    data=interface_types.query.all()
    print(data)
    return render_template("partial/interface_types_index.html", interface_types=data)

def interface_type_add():
    consoleMsg('User requested to add linecard_type')
    data = interface_types(
        description=request.form['phy_conn'],
        speed=request.form['speed']
    )
    print (data)
    db.session.add(data)
    db.session.commit()
    data=interface_types.query.all()
    print(data)
    return render_template("partial/interface_types_index.html", interface_types=data)

def interface_type_delete(interface_type_id):
    consoleMsg('User requested to delete linecard_type with id of'+str(interface_type_id))
    # Delete interface_type_id
    data = interface_types.query.get(interface_type_id)
    db.session.delete(data)
    db.session.commit()
    # Get updated linecard_type list
    data=interface_types.query.all()
    print(data)
    return render_template("partial/interface_types_index.html", interface_types=data)

###################
#
#   THE FOLLOWING SECTION IS FOR CREATING AND DELETING OF INT_PROFILE_TYPES

def int_profile_types_index():
    consoleMsg('User requested to go to int_profile_type index page')
    data=int_profile_types.query.all()
    print(data)
    return render_template("partial/int_profile_types_index.html", int_profile_types=data)

def int_profile_types_add():
    consoleMsg('User requested to add int_profile_type')
    data = int_profile_types(
        description=request.form['description'],
        profile_type=request.form['profile_type']
    )
    print (data)
    db.session.add(data)
    db.session.commit()
    data=int_profile_types.query.all()
    print(data)
    return render_template("partial/int_profile_types_index.html", int_profile_types=data)

def int_profile_types_delete(int_profile_type_id):
    consoleMsg('User requested to delete int_profile_type with id of'+str(int_profile_type_id))
    # Delete interface_type_id
    data = int_profile_types.query.get(int_profile_type_id)
    db.session.delete(data)
    db.session.commit()
    # Get updated linecard_type list
    data=int_profile_types.query.all()
    print(data)
    return render_template("partial/int_profile_types_index.html", int_profile_types=data)


###################
#
#   THE FOLLOWING SECTION IS FOR CREATING AND DELETING OF ROUTERS

def router_index():
    consoleMsg('User router index')
    # Routers, needs to be in nested if statement eventually
    data=routers.query.all()
    rtr_types=router_types.query.all()
    print ("Router list:",data)
    print ("router types:",rtr_types)
    return render_template("partial/router_index.html", routers=data, rtr_types=rtr_types )

def router_add():
    consoleMsg('User requested to create new router')
    print(request.form)
    # Add new router
    router= routers(
        name=request.form['name'],
        router_type_id=request.form['router_type_id']
    )
    db.session.add(router)
    db.session.commit()
    # Get updated router list
    data=routers.query.all()
    rtr_types=router_types.query.all()
    print ("Router list:",data)
    return render_template("partial/router_index.html", routers=data, rtr_types=rtr_types)

def router_delete(router_id):
    consoleMsg('User requested to delete router with router_id of'+str(router_id))
    # Delete router
    router_to_delete = routers.query.get(router_id)
    db.session.delete(router_to_delete)
    db.session.commit()
    # Get updated router list
    data=routers.query.all()
    rtr_types=router_types.query.all()
    return render_template("partial/router_index.html", routers=data, rtr_types=rtr_types)

def router_edit(router_id):
    consoleMsg('User requested to edit router with router_id of '+str(router_id))
    # Get router data
    data = routers.query.get(router_id)
    rtr_types=router_types.query.all()
    lc_types=linecard_types.query.all()
    int_types=interface_types.query.all()
    current_linecards=linecard_list(router_id)
    int_profiles=int_profile_types.query.all()

    return render_template("partial/router_edit.html", router=data,rtr_types=rtr_types,linecard_types=lc_types,current_linecards=current_linecards, interface_types=int_types, int_profiles=int_profiles)

def router_update(router_id):
    consoleMsg('User requested to UPDATE router with router_id of '+str(router_id))
    
    # Snag current database entries for this router + which linecards are in it, convert to dict of dicts, keyed by router_slot
    router = routers.query.get(router_id)
    current_cards=linecard_list(router_id)

    # Go through request form, compare to current cards, update/delete as needed
    print ("request form =",request.form)
    print ("starting to process request form for update")

    for key,value in request.form.items():
        if (key == "router_name") and (value != router.name):
            router.name=value
            db.session.commit()

        elif (key == "router_type_id"):
            new_router_type_id=int(value)
            if new_router_type_id != router.router_type_id:
                router.router_type_id=new_router_type_id
                db.session.commit()

                ## NOTE: IF CHANGING TO A SMALLER SIZED LINE CARD, NEED TO HANDLE FEWER ROUTER CARDS.

        # LINECARD FORM DATA
        elif 'slot' in key:
            slot=int(key[5:])
            if value == "None":
                new_linecard_type_id=None
            else:
                new_linecard_type_id=int(value)
            print("-"*40)
            print ("comparing slot number:",slot, type(slot))
            print ("new card:",new_linecard_type_id, type(new_linecard_type_id))
            try:
                old_linecard_type_id=current_cards[slot]['linecard_type_id']
            except:
                old_linecard_type_id=None
            print ("old card:",old_linecard_type_id, type(old_linecard_type_id))

            if new_linecard_type_id == old_linecard_type_id:
                print ("old and new cards are the same, no db updates needed")
            elif new_linecard_type_id == None :
                print ("need to delete old card")
                data=linecards.query.get(current_cards[slot]['router_linecard_id'])
                print ("router_linecard row to delete =",data)
                db.session.delete(data)
                db.session.commit()
            elif old_linecard_type_id == None: 
                print ("adding new router_linecard entry")
                data=linecards(
                    router_id=router_id,
                    linecard_type_id=new_linecard_type_id,
                    router_slot=slot
                )
                print (data)
                print("linecard add response=",db.session.add(data))
                db.session.commit()
            else:
                print ("updating existing router_linecard entry")
                router_linecard_id=current_cards[slot]['router_linecard_id']
                print("\n\n router_linecard_id =",router_linecard_id)
                data=linecards.query.get(router_linecard_id)
                data.linecard_type_id=new_linecard_type_id
                db.session.commit()

        # INTERFACE FORM DATA
        elif 'interface_' in key:
            print ("*"*80)
            print ("Interface data found!")

            if 'interface_type' in key:
                print ("Found interface type:",value)


            elif 'interface_profile' in key:
                print ("Found interface profile:",value)


            elif 'interface_address' in key:
                print ("Found interface address:",value)
        
            
            elif 'interface_comment' in key:
                data=re.split('_|/',key)
                slot=int(data[2])
                port=int(data[3])
                comment=value
                
                # If the comment key exists in the interface already, compare and update it; otherwise, add it.
                if ('comment' in current_cards[slot]['interfaces'][port] ):
                    print ("interface",slot,port,"has a comment key already")
                else:
                    print ("interface",slot,port,"DOES NOT have a comment key yet")

                print ("found interface comment:",value)
                print ("slot/port=",slot,"/",port)
                print ("linecard_id =",current_cards[slot])
                # if ( slot==0) and (port==0 ):
                #     print ("testing of adding interfaces data to the databse with 0/0:")
                #     data=interfaces(
                #         linecard_id=current_cards[slot]['router_linecard_id'],
                #         linecard_port_num=port,
                #         ip_address_v4="192.168.50.2/24",
                #         comment=comment               
                #     )
                #     db.session.add(data)
                #     db.session.commit()
            
    # Snagging current DB info to re-populate content window
    data = routers.query.get(router_id)
    print ("data = ",data.__dict__)
    rtr_types=router_types.query.all()
    lc_types=linecard_types.query.all()
    int_types=interface_types.query.all()
    int_profiles=int_profile_types.query.all()
    current_linecards=linecard_list(router_id)


    return render_template("partial/router_edit.html", router=data,rtr_types=rtr_types,linecard_types=lc_types,current_linecards=current_linecards, interface_types=int_types, int_profiles=int_profiles)
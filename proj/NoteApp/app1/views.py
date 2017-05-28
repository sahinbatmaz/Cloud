from django.shortcuts import render
from django.conf import settings

import os
import shutil
import re
import textwrap

# Create your views here.

def index(request):

    focusPath = request.GET['path']
    focusFullPath = settings.BASE_DIR+"/storage/data/"+focusPath

    focusInfo = []
    with open(focusFullPath+"/.init.noteapp",'r') as ff:
        ff.readline(); focusInfo.append(ff.readline().strip()); ff.readline()

    focusFiles = [];focusDirs = [];
    for (dirpath, dirnames, filenames) in os.walk(focusFullPath):
        focusFiles.extend(filenames); focusFiles.remove('.init.noteapp'); focusFiles.remove('.notes.noteapp')
        focusDirs.extend(dirnames)
        break

    focusDirNames = []
    for dir_x in focusDirs:
        with open(focusFullPath+"/"+dir_x+"/.init.noteapp",'r') as ff:
            ff.readline();focusDirNames.append(ff.readline().strip());ff.readline()

    focusLocations = []
    with open(focusFullPath+"/.locations.noteapp",'r') as ff:
        focusLocations = ''.join(ff.readlines())
        focusLocations = focusLocations.replace("\n","")


    context = {"focusPath":focusPath,
                "focusName":focusInfo[0],
                "focusDirs":focusDirs,
                "focusDirNames":focusDirNames,
                "focusFiles":focusFiles,
                "focusLocations":focusLocations }
    return render(request, 'index.html', context)

def node(request):
    noteFilePath = request.GET['path'] + "/.notes.noteapp"
    noteFullPath = settings.BASE_DIR+"/storage/data/"+ noteFilePath

    with open(noteFullPath,'r') as ff:
        notes = ''.join(ff.readlines())

    context ={"focuspath": request.GET['path'], "notes": notes }
    return render(request, 'node.html', context)

def ajax(request):

    if 'savehtml' in request.GET and 'path' in request.GET:

        focusPath = request.GET['path']
        focusFullPath = settings.BASE_DIR + "/storage/data/" + focusPath

        with open(focusFullPath+"/.notes.noteapp",'w') as ff:
            ff.write(request.GET['savehtml'])
    elif 'addnode' in request.GET and 'path' in request.GET:
        focusPath = request.GET['path']
        focusFullPath = settings.BASE_DIR + "/storage/data/" + focusPath

        with open(focusFullPath+"/.locations.noteapp" ,'r') as ff:
            locInfo = ''.join(ff.readlines())

        locInfoUpdated = re.search(r'(.+\}).+?$',locInfo,re.DOTALL).group(1)+","+textwrap.dedent("""
          {
            "x": 40,
            "y": 40,
            "id": "%d"
          }
        ]""" % (len(re.findall('"id"',locInfo)) + 1) )

        with open(focusFullPath+"/.locations.noteapp" ,'w') as ff:
            ff.write(locInfoUpdated)
        

        foldername = 0
        while(os.path.isdir(focusFullPath+"/"+str(foldername))):
            foldername += 1
        newnodeFullPath = focusFullPath+"/"+str(foldername)
        os.makedirs(newnodeFullPath)
        with open(newnodeFullPath+"/.init.noteapp",'w') as ff:
            ff.write("[filename]\n")
            ff.write("new node\n")
            ff.write("\n")
        with open(newnodeFullPath+"/.notes.noteapp",'w') as ff:
            ff.write("")
        with open(newnodeFullPath+"/.locations.noteapp",'w') as ff:
            ff.write(
             """[
                    {
                        "x": 0,
                        "y": 0,
                        "id": "1"
                    }
                ]"""
            )

    elif 'deletenode' in request.GET and 'path' in request.GET:
        focusPath = request.GET['path']
        focusFullPath = settings.BASE_DIR + "/storage/data/" + focusPath

        shutil.rmtree(focusFullPath)

        ## Remove node position from parent view
        parentPath = re.search("(.+)\/.+?",focusPath).group(1)
        parentFullPath = settings.BASE_DIR + "/storage/data/" + parentPath

        with open(parentFullPath+"/.locations.noteapp" ,'r') as ff:
            locInfo = ''.join(ff.readlines())

        tt = re.search(r'(.+)\{.+?\}(.+?$)',locInfo,re.DOTALL)
        tt2 = re.search(r'(.+),.*?$',tt.group(1),re.DOTALL)
        locInfo = tt2.group(1)+tt.group(2)

        with open(parentFullPath+"/.locations.noteapp" ,'w') as ff:
            ff.write(locInfo)
            
    elif 'editnode' in request.GET and 'path' in request.GET and 'name' in request.GET:
        focusPath = request.GET['path']
        focusFullPath = settings.BASE_DIR + "/storage/data/" + focusPath

        newFocusName = request.GET['name']

        with open(focusFullPath+"/.init.noteapp",'r') as ff:
            initFile = ff.readline()
            initFile += newFocusName
            ff.readline()
            initFile += ''.join(ff.readlines())

        with open(focusFullPath+"/.init.noteapp",'w') as ff:
            ff.write(initFile)

    elif 'exportnetwork' in request.GET and 'path' in request.GET and 'data' in request.GET:
        focusPath = request.GET['path']
        networkData = request.GET['data']

        focusFullPath = settings.BASE_DIR + "/storage/data/" + focusPath    

        with open(focusFullPath+"/.locations.noteapp",'w') as ff:
            ff.write(networkData)


    from django.http import HttpResponse
    response = HttpResponse("Here's the text of the Web page.")
    return response

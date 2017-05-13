from django.shortcuts import render
from django.conf import settings

from os import walk

# Create your views here.

def index(request):

    focusPath = request.GET['path']
    focusFullPath = settings.BASE_DIR+"/storage/data/"+focusPath

    focusInfo = []
    with open(focusFullPath+"/.init.noteapp",'r') as ff:
        ff.readline(); focusInfo.append(ff.readline().strip()); ff.readline()

    focusFiles = [];focusDirs = [];
    for (dirpath, dirnames, filenames) in walk(focusFullPath):
        focusFiles.extend(filenames); focusFiles.remove('.init.noteapp'); focusFiles.remove('.notes.noteapp')
        focusDirs.extend(dirnames)
        break

    focusDirNames = []
    for dir_x in focusDirs:
        with open(focusFullPath+"/"+dir_x+"/.init.noteapp",'r') as ff:
            ff.readline();focusDirNames.append(ff.readline().strip());ff.readline()


    context = {"focusPath":focusPath,
                "focusName":focusInfo[0],
                "focusDirs":focusDirs,
                "focusDirNames":focusDirNames,
                "focusFiles":focusFiles }
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

    from django.http import HttpResponse
    response = HttpResponse("Here's the text of the Web page.")
    return response
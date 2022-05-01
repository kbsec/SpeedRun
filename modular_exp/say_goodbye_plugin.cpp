#include <windows.h>


void SayGoodbyeAction(){
    MessageBoxA(NULL, "Goodbye!", "world!", MB_OK);
    return;
}


// This is the name of my plugin
char SayGoodbyeName[] = "SayGoodbye";

// C++ will mangle names in exported functions. This is why we use edtern "C"
extern "C" __declspec(dllexport) char* Name()
{
    return SayGoodbyeName;
}


// Action is the function we invoke from this plugin 
extern "C" __declspec(dllexport) void Action()
{
    SayGoodbyeAction();
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
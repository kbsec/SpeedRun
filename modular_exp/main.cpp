#include <windows.h>
#include <iostream> 
#include <string> 
#include <unordered_map>


typedef void PluginAction(void);
typedef char* PluginName(void);
//typedef  std::unordered_map<std::string, Plugin*> PluginTable;



struct Plugin{
    PluginName* dllName;
    PluginAction* dllAction;
    HMODULE hModule; 
};


auto sPluginx =  sizeof(Plugin);

char SayHelloName[] = "SayHello";
void SayHello(){
    MessageBoxA(NULL, "Hello!", "world!", MB_OK);
    return;

}

// Modularity: 
// 1 file that contains core functionality
// Then possibly many exes that contain plugins/extra functionality not necessarily implemented 
// in the the core executable 


std::string LoadPlugin(char* dllName,  std::unordered_map<std::string, Plugin*> *lpPluginTable ){
   
    std::string result = "";
    std::string basePath = "./plugins/";
    basePath  += std::string(dllName);
    std::cout<< basePath <<std::endl;

    HMODULE hModule  = LoadLibraryA(basePath.c_str());
    if (hModule ==NULL){
        std::cout << "Failed to get Lib because of "<< ::GetLastError() <<std::endl;
        return result;
    }
    PluginName* plgName = (PluginName* ) GetProcAddress(hModule, "Name");
    if(plgName == NULL){
        std::cout<< "Invalid plugin format! Missing `Name` function" << std::endl;
        return result;
    }
    Plugin* lpPlugin = (Plugin*) malloc(sizeof(Plugin)); 
    std::string funcName = std::string(plgName());
    std::cout << "Our new function is ..." << funcName << std::endl;

    // Added the Action, Name and Base address of our struct 
    lpPlugin->dllAction  = (PluginAction*) GetProcAddress(hModule, "Action");
    lpPlugin->dllName = plgName;
    lpPlugin->hModule = hModule;
    lpPluginTable->insert({funcName ,lpPlugin});
    return funcName;
    //;

}

void UnloadPlugin(std::string funcName, std::unordered_map<std::string, Plugin*>  *lpPluginTable ){
     auto plugin = lpPluginTable->at(funcName);
     FreeLibrary(plugin->hModule);
     std::cout << "Freeing Library " 
        << funcName 
        << " " 
        << FreeLibrary(plugin->hModule)
        << std::endl;
    lpPluginTable->erase(funcName);
    free(plugin);
}


int main(int argc, char* argv[]){
    //char dllName[] ="saygoodbye.dll";
    //PluginAction* dllAction = (PluginAction*) LoadPlugin(dllName);
    //dllAction();
     std::unordered_map<std::string, Plugin*> pluginTable = {};

    if (argc ==1){
        std::cout<< "invalid number of args" <<std::endl;
        return 0 ;
    }
    if (strcmp(argv[1],SayHelloName) ==0 ){
        SayHello();
        return 0;
    } else if(strcmp(argv[1],"LoadModule") ==0 ){
        if (argc < 3){
            std::cout << "No plugin listed!" << std::endl;
            return 0;
        }
        // 3rd argument, specifying the dll name 
        char *dllName = argv[2];
        std::string funcName = LoadPlugin(dllName, &pluginTable);
        if(funcName.length() != 0){
            //

            auto plugin = pluginTable.at(funcName);
            plugin->dllAction();
            UnloadPlugin(funcName,  &pluginTable);

        }
        

    } else{
        std::cout<< "I dont know what this is!" <<std::endl;
    } 
    std::cout << "Goodbye!" << std::endl;
    return 0;
}


/*

*/
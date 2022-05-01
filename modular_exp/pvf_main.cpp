#include <windows.h>
#include <string>
#include <iostream>

class Command{
    public:
        virtual std::string Name() = 0;
        virtual std::string Action() = 0; 

};


class GetUsername : Command {
    public:
        //GetUsername();
        std::string Name(){ return std::string("GetUsername");}
        std::string Action(){
            DWORD dwSize = 0;
            /*
            BOOL GetUserNameA(
                [out]     LPSTR   lpBuffer,
                [in, out] LPDWORD pcbBuffer
                );
            */
            GetUserNameA(NULL, &dwSize);
            char* buffer = new char[dwSize];
            GetUserNameA(buffer, &dwSize);
            std::string result(buffer);
            delete [] buffer;
            return result;
        }
};


int main(){
    Command* gu = NULL;
    gu = (Command*) new GetUsername();
    auto res = gu->Action();
    std::cout << gu->Name() << std::endl;
    std::cout << res << std::endl;

}
CXX=clang++



main:
	$(CXX) main.cpp -lUser32 -o main.exe

pvf_main:
	$(CXX) pvf_main.cpp -lUser32 -lAdvapi32 -o pvf_main.exe


saygoodbye:
	$(CXX) say_goodbye_plugin.cpp -lUser32 -shared -o plugins/saygoodbye.dll

telljoke:
	$(CXX) telljoke_plugin.cpp -lUser32 -shared -o plugins/telljoke.dll

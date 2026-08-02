#import <Foundation/Foundation.h>
#import <dlfcn.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    @autoreleasepool {
        NSString *gadget = @"/usr/lib/FridaGadget.dylib";
        void *handle = NULL;
        for (int i = 0; i < 30 && !handle; i++) {
            handle = dlopen([gadget UTF8String], RTLD_NOW);
            if (!handle) {
                usleep(500000);
            }
        }
        while (1) {
            sleep(1);
        }
    }
    return 0;
}

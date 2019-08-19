/*
   XHC-WHB04B-6 Wireless MPG pendant LinuxCNC HAL module for LinuxCNC.
   Based on XHC-HB04.

   Copyright (C) 2018 Raoul Rubien (github.com/rubienr).

   This program is free software; you can redistribute it and/or
   modify it under the terms of the GNU Lesser General Public
   License as published by the Free Software Foundation; either
   version 2 of the License, or (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   Lesser General Public License for more details.

   You should have received a copy of the GNU Lesser General Public
   License along with the program; if not, write to the Free
   Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
   02111-1307 USA.
 */

// system includes
#include <iostream>
#include <sstream>
#include <unistd.h>
#include <signal.h>

// 3rd party includes
#include <google/protobuf/stubs/common.h>

// local library includes

// local includes
#include "./xhc-whb04b6.h"

// forward declarations

// globals
//! link object for signal handler
XhcWhb04b6::XhcWhb04b6Component* WhbComponent{nullptr};

// ----------------------------------------------------------------------

static int printUsage(const char* programName, const char* deviceName, bool isError = false)
{
    std::ostream* os = &std::cout;
    if (isError)
    {
        os = &std::cerr;
    }
    *os << programName << " version " << PACKAGE_VERSION << " " << __DATE__ << " " << __TIME__ << "\n"
        << "\n"
        << "SYNOPSIS\n"
        << "    " << programName << " [-h | --help] | [-H] [OPTIONS]\n"
        << "\n"
        << "NAME\n"
        << "    " << programName << " - jog dial HAL component for the " << deviceName << " device\n"
        << "\n"
        << "DESCRIPTION\n"
        << "    " << programName << " is a HAL component that receives events from the " << deviceName << " device "
        << "and exposes them to HAL via HAL pins.\n"
        << "\n"
        << "OPTIONS\n"
        << " -h, --help\n"
        << "    Prints the synopsis and the most commonly used commands.\n"
        << "\n"
        << " -H\n"
        << "    Run " << programName << " in HAL-mode instead of interactive mode. When in HAL mode "
        << "commands from device will be exposed to HAL's shred memory. Interactive mode is useful for "
        << "testing device connectivity and debugging.\n"
        << "\n"
        << " -t\n"
        << "    Wait with timeout for USB device then proceed, exit otherwise. Without -t the timeout is "
        << "implicitly infinite.\n"
        << "\n"
        << " -s, \n"
        << "    Lead in Spindle mode: "
        << "Lead + jogwheel changes the spindle speed. Each tick will increase/decrease the spindle speed.\n"
        << "\n"
        << " -f, \n"
        << "    Lead in Feed mode: "
        << "Lead + jogwheel changes the feed override. Each tick will increment/decrement the feed override.\n"
        << "\n"
        << " -u, -U\n"
        << "    Show received data from device. With -U received and transmitted data will be printed. "
        << "Output is prefixed with \"usb\".\n"
        << "\n"
        << " -p\n"
        << "    Show HAL pins and HAL related messages. Output is prefixed with \"hal\".\n"
        << "\n"
        << " -e\n"
        << "    Show captured events such as button pressed/released, jog dial, axis rotary button, and "
            "feed rotary button event. Output is prefixed with \"event\".\n"
        << "\n"
        << " -a\n"
        << "    Enable all logging facilities without explicitly specifying each.\n"
        //! this feature must be removed when checksum check is implemented
        << "\n"
        << " -c\n"
        << "    Enable checksum output which is necessary for debugging the checksum generator function. Do not rely "
            "on this feature since it will be removed once the generator is implemented.\n"
        << "\n"
        << " -n\n"
        << "    Force being silent and not printing any output except of errors. This will also inhibit messages "
            "prefixed with \"init\".\n"
        << "\n"
        << "EXAMPLES\n"
        << programName << " -ue\n"
        << "    Start in userspace mode (simulation) and prints incoming USB data transfer and generated key pressed/released events.\n"
        << "\n"
        << programName << " -p\n"
        << "    Start in userspace mode (simulation) and prints HAL pin names and events distributed to HAL memory.\n"
        << "\n"
        << programName << " -Hn\n"
        << "    Start in HAL mode and avoid output, except of errors.\n"
        << "\n"
        << "AUTHORS\n"
        << "    This component was started by Raoul Rubien based on predecessor "
           "device's component xhc-hb04.cc. https://github.com/machinekit/machinekit/graphs/contributors "
           "gives you a more complete list of contributors."
        << "\n";
    if (isError)
    {
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}

// ----------------------------------------------------------------------
//! called on program termination requested
static void quit(int signal)
{
    if (WhbComponent != nullptr)
    {
        WhbComponent->requestTermination(signal);
    }
}

// ----------------------------------------------------------------------

//! registers signal handler
void registerSignalHandler()
{
    signal(SIGINT, quit);
    signal(SIGTERM, quit);
}

// ----------------------------------------------------------------------

bool parseFloat(const char* str, float& out)
{
    std::istringstream iss(str);
    if (!(iss >> out))
    {
        std::cerr << "no valid value specified: " << str << "\n";
        return false;
    }
    return true;
}

// ----------------------------------------------------------------------

int main(int argc, char** argv)
{
    WhbComponent = new XhcWhb04b6::XhcWhb04b6Component();

    const char* optargs = "phaeHuctnUs:v:";
    for (int opt = getopt(argc, argv, optargs); opt != -1; opt = getopt(argc, argv, optargs))
    {
        switch (opt)
        {
            case 'H':
                WhbComponent->setSimulationMode(false);
                break;
            case 't':
                WhbComponent->setWaitWithTimeout(3);
                break;
            case 'e':
                WhbComponent->enableVerbosePendant(true);
                WhbComponent->setEnableVerboseKeyEvents(true);
                break;
            case 'u':
                WhbComponent->enableVerboseInit(true);
                WhbComponent->enableVerboseRx(true);
                break;
            case 'U':
                WhbComponent->enableVerboseInit(true);
                WhbComponent->enableVerboseRx(true);
                WhbComponent->enableVerboseTx(true);
                break;
            case 'p':
                WhbComponent->enableVerboseInit(true);
                WhbComponent->enableVerboseHal(true);
                break;
            case 'a':
                WhbComponent->enableVerboseInit(true);
                WhbComponent->enableVerbosePendant(true);
                WhbComponent->setEnableVerboseKeyEvents(true);
                WhbComponent->enableVerboseRx(true);
                WhbComponent->enableVerboseTx(true);
                WhbComponent->enableVerboseHal(true);
                break;
            case 'c':
                WhbComponent->enableCrcDebugging(true);
                break;
            case 's':
                WhbComponent->setLeadModeSpindle();
                break;
            case 'f':
                WhbComponent->setLeadModeFeed();
                break;
            case 'n':
                break;
            case 'h':
                return printUsage(basename(argv[0]), WhbComponent->getName());
                break;
            default:
                return printUsage(basename(argv[0]), WhbComponent->getName(), true);
                break;
        }
    }

    registerSignalHandler();

    WhbComponent->run();

    //! hotfix for https://github.com/machinekit/machinekit/issues/1266
    if (WhbComponent->isSimulationModeEnabled())
    {
        google::protobuf::ShutdownProtobufLibrary();
    }

    delete (WhbComponent);
    return 0;
}

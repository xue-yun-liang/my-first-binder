from subprocess import Popen, PIPE
from getevaluation import getevaluation
import time
import os
import math
import subprocess


def evaluation(status):
    core = str(status["core"])
    benchmarksize = ""
    l1i_size = str(int(math.pow(2, int(status["l1i_size"]))))
    l1d_size = str(int(math.pow(2, int(status["l1d_size"]))))
    l2_size = str(int(math.pow(2, int(status["l2_size"]))))
    l1d_assoc = str(int(math.pow(2, status["l1d_assoc"])))
    l1i_assoc = str(int(math.pow(2, status["l1i_assoc"])))
    l2_assoc = str(int(math.pow(2, status["l2_assoc"])))
    sys_clock = str(status["sys_clock"])
    print(core)
    print(l1i_size)
    print(l1d_size)
    print(l2_size)
    print(l1d_assoc)
    print(l1i_assoc)
    print(l2_assoc)
    print(sys_clock)
    # core = "3"
    # benchmarksize =""
    # l1i_size ="256"
    # l1d_size ="256"
    # l2_size="64"
    # l1d_assoc="8"
    # l1i_assoc="8"
    # l2_assoc="8"
    # sys_clock="2"
    start = time.time()
    print("++++++++++++++++++++++++++starsimulatr+++++++++++++++++++++++++++++++")

    os.system(
        "/parsec-tests2/gem5_2/gem5/build/X86/gem5.fast -re /parsec-tests2/gem5_2/gem5/configs/example/fs.py --script=/parsec-tests2/parsec-image/benchmark_src/canneal_{}c_simdev.rcS -F 5000000000  --cpu-type=TimingSimpleCPU --num-cpus={} --sys-clock='{}GHz' --caches --l2cache   --l1d_size='{}kB' --l1i_size='{}kB' --l2_size='{}kB' --l1d_assoc={} --l1i_assoc={} --l2_assoc={} --kernel=/parsec-tests2/parsec-image/system/binaries/x86_64-vmlinux-2.6.28.4-smp --disk-image=/parsec-tests2/parsec-image/system/disks/x86root-parsec.img".format(
            core,
            core,
            sys_clock,
            l1d_size,
            l1i_size,
            l2_size,
            l1d_assoc,
            l1i_assoc,
            l2_assoc,
        )
    )
    # os.system("/parsec-tests2/gem5_2/gem5/build/X86/gem5.fast  -re  /parsec-tests2/gem5_2/gem5/configs/example/fs.py --script=/parsec-tests2/parsec-image/benchmark_src/blackscholes_2c_simdev.rcS -F 5000000000  --cpu-type=TimingSimpleCPU --num-cpus=2 --sys-clock='2.2GHz' --caches --l2cache   --l1d_size='128kB' --l1i_size='128kB' --l2_size='512kB' --l1d_assoc=8 --l1i_assoc=8 --l2_assoc=8 --kernel=/parsec-tests2/parsec-image/system/binaries/x86_64-vmlinux-2.6.28.4-smp --disk-image=/parsec-tests2/parsec-image/system/disks/x86root-parsec.img")
    bar = "========================="
    print(bar, "endsimulatr", bar)

    print(bar + "startdevore", bar)
    f1 = open("/m5out/stats.txt")
    ss = bar + "Begin Simulation Statistics " + bar
    sr = f1.read().split(ss)
    f1.close()
    for i in range(len(sr)):
        f = open("/m5out/%d.txt" % i, "w")
        f.write(sr[i] if i == 0 else ss + sr[i])
        f.close()

    print(bar, "end devore", bar)
    try:

        if os.path.exists("/m5out/3.txt"):
            print(bar, "startGEM5ToMcPAT", bar)
            command_2 = [
                "python3",
                "/parsec-tests2/cmcpat/cMcPAT/Scripts/GEM5ToMcPAT.py",
                "/m5out/3.txt",
                "/m5out/config.json",
                "/parsec-tests2/cmcpat/cMcPAT/mcpat/ProcessorDescriptionFiles/x86_AtomicSimpleCPU_template_core_{}.xml".format(
                    core
                ),
                "-o",
                "/parsec-tests2/cmcpat/cMcPAT/Scripts/test.xml",
            ]
            process2 = Popen(command_2)
            process2.wait()
            print(bar, "endGEM5ToMcPAT", bar)
            print(bar, "startMcPAT", bar)

            file_output = open(
                "/parsec-tests2/cmcpat/cMcPAT/mcpatresult/test2.log", "w"
            )
            command_3 = [
                "/parsec-tests2/cmcpat/cMcPAT/mcpat/mcpat",
                "-infile",
                "/parsec-tests2/cmcpat/cMcPAT/Scripts/test.xml",
                "-print_level",
                "5",
            ]
            process3 = Popen(command_3, stdout=file_output)
            process3.wait()
            print(bar, "endMcPAT", bar)
            print(bar, "startprintenergy", bar)
            # command_4 = ["python3","/parsec-tests2/cmcpat/cMcPAT/Scripts/print_energy.py" ,"/parsec-tests2/cmcpat/cMcPAT/mcpatresult/test2.log","/parsec-tests2/gem5_2/gem5/m5out/3.txt"]
            # process4 = Popen(command_4)
            # process4.wait()
            metrics = getevaluation(
                "/parsec-tests2/cmcpat/cMcPAT/mcpatresult/test2.log", "/m5out/3.txt"
            )
            print(bar, "endprintenergy", bar)
            os.remove("/m5out/3.txt") if os.path.exists("/m5out/3.txt") else None
            (
                os.remove("/parsec-tests2/cmcpat/cMcPAT/mcpatresult/test2.log")
                if os.path.exists("/parsec-tests2/cmcpat/cMcPAT/mcpatresult/test2.log")
                else None
            )
            (
                os.remove("/parsec-tests2/cmcpat/cMcPAT/Scripts/test.xml")
                if os.path.exists("/parsec-tests2/cmcpat/cMcPAT/Scripts/test.xml")
                else None
            )
            end = time.time()
            print("程序process_1的运行时间为：{}".format(end - start))
            return metrics
        else:
            return None
    except:
        os.remove("/m5out/3.txt") if os.path.exists("/m5out/3.txt") else None
        (
            os.remove("/parsec-tests2/cmcpat/cMcPAT/mcpatresult/test2.log")
            if os.path.exists("/parsec-tests2/cmcpat/cMcPAT/mcpatresult/test2.log")
            else None
        )
        (
            os.remove("/parsec-tests2/cmcpat/cMcPAT/Scripts/test.xml")
            if os.path.exists("/parsec-tests2/cmcpat/cMcPAT/Scripts/test.xml")
            else None
        )
        print(f"current status can't be evaluated")
        return None


# cheackdik = dict()
# cheackdik['core']=16
# cheackdik['l1i_size']=10
# cheackdik['l1d_size']=10
# cheackdik['l2_size']=7
# cheackdik['l1d_assoc']=8
# cheackdik['l1i_assoc']=8
# cheackdik['l2_assoc']=8
# cheackdik['sys_clock']=2
# metrics=evaluation(cheackdik)
# print (metrics)

import platform
import sys
import psutil

def get_system_info():
    info = {}

    # Plataform
    info['system'] = platform.system()
    info['release'] = platform.release()
    info['version'] = platform.version()
    info['machine'] = platform.machine()
    info['processor'] = platform.processor()

    # memory
    mem = psutil.virtual_memory()
    info['total_memory_gb'] = round(mem.total / (1024 ** 3), 2)

    # python lang info
    info['python_version'] = sys.version
    info['python_implementation'] = sys.implementation.name

    return info

def system_info_main():
    system_info = get_system_info()
    output_filename = "system_info.txt"

    try:
        with open(output_filename, "w") as outfile:
            outfile.write("System Information:\n")
            for key, value in system_info.items():
                outfile.write(f"- {key.replace('_', ' ').title()}: {value}\n")
        print(f"System information has been saved to '{output_filename}'")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")


if __name__ == "__main__":
    system_info_main()
from functions.get_files_info import get_files_info


class main():
    rootContent = get_files_info("calculator", ".")
    print(rootContent)

    pkgContent = get_files_info("calculator", "pkg")
    print(pkgContent)

    binContent = get_files_info("calculator", "bin")
    print(binContent)

    prevContent = get_files_info("calculator", "../")
    print(prevContent)


main()

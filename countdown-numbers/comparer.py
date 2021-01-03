
with open('main.result.txt') as f:
    main_results = [line.rstrip() for line in f]
with open('novel.result.txt') as f:
    novel_results = [line.rstrip() for line in f]

novel_not_in_main = [item for item in novel_results if item not in main_results]
main_not_in_novel = [item for item in main_results if item not in novel_results]

with open('comparison.result.txt', 'w') as f:
    f.write('novel results not in main:\n')
    f.write('\n'.join(novel_not_in_main))

    f.write('main results not in novel:\n')
    f.write('\n'.join(main_not_in_novel))

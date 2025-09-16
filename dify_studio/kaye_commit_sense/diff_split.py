def main(input):
    DIFF_GIT = "diff --git"
    segments = input.split(DIFF_GIT)
    result_list = []
    for segment in segments[1:]:
        result_list.append(DIFF_GIT + segment)

    return {"output": result_list, "file_count": len(result_list)}

import os
import json
import customize


FILE = "scores.json"


def create_score_file():
    try:
        file = open(FILE, "w")
        json.dump({"profiles": []}, file)
        file.close()
    except IOError as e:
        print(e)


def open_score_file(access_type="r"):
    if os.path.exists(FILE):
        try:
            return open(FILE, access_type)
        except IOError as e:
            print(e)
            return None
    else:
        create_score_file()


def get_JSON(file):
    try:
        return json.load(file)
    except Exception as e:
        print(e)
        return dict()


def write_to_file(json_dict: dict):
    over_file = open_score_file("w")
    json.dump(json_dict, over_file, indent=4)
    over_file.close()


def get_profiles():
    profile_list = []
    file = open_score_file()
    if file is not None:
        json_dict: dict = get_JSON(file)
        if json_dict is not None:
            if "profiles" in json_dict:
                if type(json_dict["profiles"]) == list:
                    for prof in json_dict["profiles"]:
                        if "name" in prof:
                            profile_list.append(prof["name"])
    if file is not None:
        file.close()
    return profile_list


def get_scores(profile: str):
    score_list = []
    file = open_score_file()
    if file is not None:
        json_dict: dict = get_JSON(file)
        file.close()
        if json_dict is not None:
            if "profiles" in json_dict:
                if type(json_dict["profiles"]) == list:
                    for prof in json_dict["profiles"]:
                        if "name" in prof and prof["name"] == profile and "scores" in prof and type(prof["scores"]) == list:
                            for score in prof["scores"]:
                                score_list.append(score)
    return score_list


def append_profile(profile: str, board_size, turns_count):
    file = open_score_file()
    json_dict = get_JSON(file)
    file.close()
    if "profiles" in json_dict:
        if type(json_dict["profiles"]) == list:
            scores = [0, 0, 0, 0, 0, 0, 0]
            scores[board_size-3] = turns_count
            json_dict["profiles"].append({"name": profile, "scores": scores})
            write_to_file(json_dict)


def add_score(profile: str, board_size, turns_count):
    file = open_score_file()
    json_dict = get_JSON(file)
    file.close()
    if "profiles" in json_dict:
        if type(json_dict["profiles"]) == list:
            profile_found = False
            for prof in json_dict["profiles"]:
                if "name" in prof and prof["name"] == profile:
                    profile_found = True
                    prof["scores"][board_size - 3] = turns_count
                    write_to_file(json_dict)
                    break
            if not profile_found:
                append_profile(profile, board_size, turns_count)
    else:
        create_score_file()
        append_profile(profile, board_size, turns_count)

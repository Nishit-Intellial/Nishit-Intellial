import json


class Util(object):
    @staticmethod
    def fulltext_str_to_words(content):
        words = set()
        # words = []
        for word in content.lower().split(" "):
            word = word.strip("'")
            if len(word) >= 2:
                words.add(word)
        return words
        # return words - Util.STOP_WORDS

    @staticmethod
    def get_post_data(request):
        if request.POST.get("postData"):
            json_data = json.loads(request.POST["postData"])
            data = {}
            for d in json_data:
                data[d["name"]] = d["value"]
            return data
        else:
            return request.POST

    @staticmethod
    def get_sort_column(data, default_col="id"):
        if data["order"]:
            sort_col_index = int(data["order"][0]["column"]) if data["order"] else 0
            sort_dir = data["order"][0]["dir"] if data["order"] else "desc"
            sort_col = data["columns"][sort_col_index]["data"] if data["columns"] else None
            sort_dir = sort_dir if sort_col is not None else "desc"
            sort_col = default_col if sort_col is None else sort_col
            sort_col = "-" + sort_col if sort_dir == "desc" else sort_col
            return sort_col
        else:
            return "-" + default_col

def add_provenance(res):
    res["provenance"] = {"policy":"OPA v1","dlp":"basic_masks_v1"}
    return res

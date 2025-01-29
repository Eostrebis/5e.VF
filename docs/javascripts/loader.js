function updateSort(edit_title=true){
    document.querySelectorAll(".base-block").forEach(block => {
        block.classList.remove("unsel");
        block.classList.add("sel");
    });
    document.querySelectorAll(".button").forEach(button => {
        id = button.id.slice(0,-1);
        if (window[id]){
            button.classList.remove("off");
            button.classList.add("on");
            if (window[id] === true){
                document.querySelectorAll(".base-block:not(."+id+")").forEach(sub_block => {
                    sub_block.classList.remove("sel");
                    sub_block.classList.add("unsel");
                })
            } else {
                document.querySelectorAll(".base-block:not(."+id+"-"+window[id]+")").forEach(sub_block => {
                    sub_block.classList.add("unsel");
                    sub_block.classList.remove("sel");
                })
            }
        } else {
            button.classList.remove("on");
            button.classList.add("off");
        }
    });
    if (edit_title){
        let title = document.querySelector("h1");
        let title_text = title.textContent;
        if (title_text.includes("(")){
            title_text = title_text.substring(0,title_text.indexOf("("));
        }
        title_text = title_text + "(" + (document.querySelectorAll(".base-block").length - document.querySelectorAll(".unsel").length) +")";
        title.textContent = title_text;
    }
}

function loadJson(page_json, redirection=true, div_id=null, onclik=null) {
    fetch('../' + page_json + '.json')
        .then((response) => response.json())
        .then((json) => {
            json.sort.forEach(sort => {
                if (sort.button) {
                    button = document.createElement("button");
                    button.classList.add("button");
                    button.classList.add("off");
                    button.id = sort.name + "b";
                    switch (sort.type) {
                        case "bool":
                            window[sort.name] = false;
                            button.textContent = sort.text;
                            if (sort.icon) {
                                window[sort.name + "_img"] = sort.icon
                            }
                            break;
                        case "choice":
                            window[sort.name] = "";
                            button.textContent = sort.texts[0]
                            if (sort.icons) {
                                for (const [index, element] of sort.possibles.entries()) {
                                    window[sort.name + "_" + element + "_img"] = sort.icons[index];
                                }
                            }
                            break;
                        default:
                            window[sort.name] = 0;
                    }
                    button.onclick = function () {
                        switch (sort.type) {
                            case "bool":
                                window[sort.name] = !window[sort.name];
                                break;
                            case "choice":
                                if (window[sort.name] === "") {
                                    window[sort.name] = sort.possibles[0];
                                } else {
                                    index = sort.possibles.indexOf(window[sort.name]);
                                    if (index === sort.possibles.length - 1) {
                                        window[sort.name] = ""
                                    } else {
                                        window[sort.name] = sort.possibles[(index + 1) % (sort.possibles.length)];
                                    }
                                }
                                if (sort.texts) {
                                    if (window[sort.name] === "") {
                                        document.getElementById(sort.name + "b").textContent = sort.texts[0];
                                    }
                                    for (const [index, element] of sort.possibles.entries()) {
                                        console.log(index, element, window[sort.name]);
                                        if (element === window[sort.name]) {
                                            document.getElementById(sort.name + "b").textContent = sort.texts[index + 1];
                                        }
                                    }
                                }
                        }
                        updateSort(div_id==null);
                    };
                    if (div_id){
                        document.getElementById(div_id).appendChild(button);
                    } else {
                        document.getElementsByClassName("md-content__inner")[0].appendChild(button);
                    }
                }
            });
            base_grid = document.createElement("div");
            base_grid.classList.add("grid");
            json.options.forEach(option => {
                block = document.createElement("a");
                if (redirection) {
                    block.href = page_json + option.name;
                    block.onclick = null;
                } else {
                    block.href = "javascript:;";
                    block.onclick = onclik;
                }
                block.classList.add("base-block");
                let img = document.createElement("img");
                img.classList.add("base-img");
                img.src = "../Illustrations/" + page_json + "/" + option.name + "." + option['img-type'];
                block.appendChild(img);
                let desc = document.createElement("div");
                desc.classList.add("base-desc");
                let name = document.createElement("div");
                name.classList.add("base-name");
                name.textContent = option.name;
                let content = document.createElement("div");
                content.classList.add("base-content");
                content.textContent = option.description;
                desc.appendChild(name);
                desc.appendChild(content);
                block.appendChild(desc);
                document.querySelectorAll(".button").forEach(button => {
                    id = button.id.slice(0, -1);
                    if (option[id]) {
                        if (option[id] === true) {
                            block.classList.add(id)
                            if (window[id + "_img"]) {
                                var sub_icon = document.createElement("img");
                                sub_icon.classList.add("icon")
                                sub_icon.src = "../Illustrations/" + window[id + "_img"];
                                name.appendChild(sub_icon);
                            }
                        } else {
                            option[id].forEach(opt => {
                                block.classList.add(id + '-' + opt)
                                if (window[id + "_" + opt + "_img"]) {
                                    var sub_icon = document.createElement("img");
                                    sub_icon.classList.add("icon")
                                    sub_icon.src = "../Illustrations/" + window[id + "_" + opt + "_img"];
                                    name.appendChild(sub_icon);
                                }

                            });
                        }
                    }
                });
                base_grid.appendChild(block);
            });
            if (div_id){
                document.getElementById(div_id).appendChild(base_grid);
            } else {
                document.getElementsByClassName("md-content__inner")[0].appendChild(base_grid);
            }

        });
}

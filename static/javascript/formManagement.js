/*let categories = 0;
let ingredients = 0
let newIngredients = 0
let steps = 0*/

function setter(id, number) {
    let list = document.querySelectorAll(`[id^=id]`)

    for (let i = 0; i < list.length; i++) {

        list[i].querySelectorAll("input,select,textarea").forEach(
            function (e, item) {
                let oldName = e.getAttribute("name")
                let oldId = e.getAttribute("id")
                oldName = oldName.replace(i, i + `${number}`);
                oldId = oldId.replace(i, i + `${number}`);
                e.setAttribute("name", oldName)
                e.setAttribute("id", oldId)
            }
        )

        list[i].querySelector("span").innerHTML = list[i].querySelector("span").innerHTML.replace("1", `${i + 1}`)
        list[i].id = id + `${i}`
    }
}

function cloneMore(element = 'ingredient') {
    let newElement;
    newElement = document.getElementsByClassName(element)[0].cloneNode(true);
    var total = Number(document.querySelector(`[id^=${"id_" + element + "-TOTAL_FORMS"} ]`).value)
    let count = total + 1
    document.querySelector(`[id^=${"id_" + element + "-TOTAL_FORMS"} ]`).value = count
    newElement.querySelectorAll("input,select,textarea").forEach(
        function (i, item) {
            //Clear the input’s value
            i.value = "";
            let oldName = i.getAttribute("name")
            let oldId = i.getAttribute("id")
            oldName = oldName.replace(0, total);
            oldId = oldId.replace(0, total);
            i.setAttribute("name", oldName)
            i.setAttribute("id", oldId)
        }
    )
    newElement.querySelector("button").setAttribute("onClick", `deleteForm(${count - 1},'${element}')`)
    let spanValue = newElement.querySelector("span").innerHTML.replace(1, `${count}`)
    newElement.querySelector("span").innerHTML = spanValue
    newElement.id = element + `${count - 1}`
    $(newElement).insertAfter($(document.getElementsByClassName(element)[`${count - 2}`]));
}

function deleteForm(formNum, element = 'ingredient') {
    var totalForms = Number(document.querySelector(`[id^=${"id_" + element + "-TOTAL_FORMS"} ]`).value)
    if (totalForms <= 1) {
        return
    }
    totalForms--;
    document.querySelector(`[id^=${"id_" + element + "-TOTAL_FORMS"} ]`).value = totalForms
    const collection = document.querySelectorAll(`#${element}${formNum}`)

    for (let i = 0; i < collection.length; i++) {
        collection[i].remove();
    }
    let forms = document.querySelectorAll(`[id^=${element}]`)

    for (k = 0; k < totalForms; k++) {
        forms[k].querySelector("span").innerHTML = `${element}${k + 1}` + " :";
        forms[k].querySelector("button").setAttribute("onClick", `deleteForm(${k},'${element}')`)

        forms[k].setAttribute('id', element + `${k}`)
        forms[k].querySelectorAll("input,select,textarea").forEach(
            function (i, item) {
                let oldName = i.getAttribute("name")
                let oldId = i.getAttribute("id")
                let numberPart = oldId.match(/\d+/g);
                i.setAttribute("id", (oldId.replace(numberPart, k + "")));
                i.setAttribute("name", (oldName.replace(numberPart, k + "")));
                let newName = i.getAttribute("name")
                let newId = i.getAttribute("id")
            }
        )
    }
}

let categories = 0;
let ingredients = 0
let newIngredients = 0
let steps = 0

function setter(id,number) {
    //  let total=Number($("input[id='id_form-TOTAL_FORMS']").attr('value'))

    let list = document.querySelectorAll(`[id^=id]`)
    //let count

    for (let i = 0; i < list.length; i++) {

        list[i].querySelectorAll("input,select,textarea").forEach(
            function (e, item) {
                //Clear the input’s value
                //i.value="";
                let oldName = e.getAttribute("name")
                let oldId = e.getAttribute("id")
                //I’d like to replace the numeric value only with the total value
                //Update the “id and name” attributes of each element
                oldName=oldName.replace(i, i+`${number}`) ;
                oldId=oldId.replace(i, i+`${number}`) ;
                e.setAttribute("name",oldName)
                e.setAttribute("id",oldId)
            }
        )

        list[i].querySelector("span").innerHTML = list[i].querySelector("span").innerHTML.replace("1", `${i + 1}`)
        list[i].id = id + `${i}`
    }
}

function cloneMore(element = 'ingredient') {
    let newElement;

    newElement = document.getElementsByClassName(element)[0].cloneNode(true);
    // update the management form
    var total = Number($("input[id='id_form-TOTAL_FORMS']").attr('value'))
    let count = total + 1
    Number($("input[id='id_form-TOTAL_FORMS']").attr('value', count + ""))
    let items = ingredients
    if (element === 'ingredient') {
        ingredients++
        items = ingredients
    } else if (element === 'newingredient') {
        newIngredients++
        items = newIngredients
        total = Number($("input[id='id_recipeingredient_set-TOTAL_FORMS']").attr('value'))
        count--
        Number($("input[id='id_form-TOTAL_FORMS']").attr('value', count + ""))
        count = total + 1
        Number($("input[id='id_recipeingredient_set-TOTAL_FORMS']").attr('value', count + ""))
    } else if (element === 'category') {
        categories++
        items = categories
    } else if (element === 'step') {
        steps++
        items = steps
    }


    // Updating the input fields are really important and especially the name attributes
    // loop over each input in the new cloning element
    newElement.querySelectorAll("input,select,textarea").forEach(
        function (i, item) {
            //Clear the input’s value
            i.value = "";
            let oldName = i.getAttribute("name")
            let oldId = i.getAttribute("id")
            //I’d like to replace the numeric value only with the total value
            //Update the “id and name” attributes of each element
            oldName = oldName.replace(0, total);
            oldId = oldId.replace(0, total);
            i.setAttribute("name", oldName)
            i.setAttribute("id", oldId)
        })

    // update the delete button index value
    newElement.querySelector("button").setAttribute("onClick", `deleteForm(${items},'${element}')`)
    // update the span index value
    let spanValue = newElement.querySelector("span").innerHTML.replace(1, `${items + 1}`)
    newElement.querySelector("span").innerHTML = spanValue
    newElement.id = element + `${total}`
    // insert the newElement at the end
    $(newElement).insertAfter($(document.getElementsByClassName(element)[`${items - 1}`]));
}

function deleteForm(formNum, element = 'ingredient') {
    // Get the current total of forms
    var totalForms = Number($("input[id='id_form-TOTAL_FORMS']").attr('value'))
    let number
    // Decrement the totalForms variable by one and update the
    if (element === 'ingredient') {
        number = ingredients
    } else if (element === 'newingredient') {
        number = newIngredients
    } else if (element === 'category') {
        number = categories
    } else if (element === 'step') {
        number = steps
    }
    if (number <= 0) {
        return
    }
    totalForms--;
    number--
    $("input[id='id_form-TOTAL_FORMS']").attr('value', totalForms);
    if (element === 'ingredient') {
        ingredients--
    } else if (element === 'newingredient') {
        Number($("input[id='id_form-TOTAL_FORMS']").attr('value', `${totalForms + 1}` + ""))
        totalForms = Number($("input[id='id_recipeingredient_set-TOTAL_FORMS']").attr('value'))
        totalForms--;
        Number($("input[id='id_recipeingredient_set-TOTAL_FORMS']").attr('value', totalForms + ""))
        newIngredients--
    } else if (element === 'category') {
        categories--
    } else if (element === 'step') {
        steps--
    }
    // Prevent deleting all forms, keep one form
    const collection = document.querySelectorAll(`#${element}${formNum}`)

    for (let i = 0; i < collection.length; i++) {
        collection[i].remove();
    }
    let forms = document.querySelectorAll(`[id^=${element}]`)

    for (k = 0; k <= number; k++) {
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
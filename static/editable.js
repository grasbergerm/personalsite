$.fn.editable = function() {
            var textBlocks = $(this);

            // Create a new input for every div that is selected
            // .my-text-box class is added so we can attach events to this class :) there is other approaches too.
            for(var i = 0; i < textBlocks.length; i+=1){
                var textBox = $('<input class="input-text-box"/>');
                var textBlock = textBlocks.eq(i);
                textBox.hide().insertAfter(textBlock);
                if (!textBlock.hasClass("blank")) {
                    textBox.val(textBlock.html())
                }
            }

            // Hiding the div and showing a input to allow editing the value.
            textBlocks.dblclick(function() {
                toggleVisiblity($(this), true); // Pass the dbl clicked div element via $(this)
            });

            // Hiding the input and showing the original div
            $('.input-text-box').blur(function() {
                toggleVisiblity($(this), false); // Pass the input that loses focus via $(this)
            });

            toggleVisiblity = function(element, editMode) {
                var textBlock,
                    textBox;

                if (editMode === true) {
                    textBlock = element; // here the element is the div
                    textBox = element.next(); // here element is the div so the textbox is next
                    textBlock.hide();
                    textBox.show().focus();
                    // workaround, to move the cursor at the end in input box.
                    textBox[0].value = textBox[0].value;
                } else {
                    textBlock = element.prev(); // Here element is the input so the div is previous
                    textBox = element; // here element is the textbox
                    textBlock.show();
                    textBox.hide();

                    if(!textBlock.hasClass("blank") && textBox.val()) {
                        textBlock.html(textBox.val());
                    } else if (textBlock.hasClass("blank") && textBox.val()) {
                        textBlock.html(textBox.val());
                        textBlock.removeClass("blank");
                    } else {
                        var element_name_array = textBlock.attr("id").split("_")
                        element_name_array = element_name_array.filter(function(result) {
                            return result != "display" && result != 'value';
                        });
                        element_name_array = $.each(element_name_array, function(index, item) {
                            element_name_array[index] = item.slice(0,1).toUpperCase() + item.slice(1);
                        });
                        textBlock.html("Double click to add " + element_name_array.join(" "))
                        textBlock.addClass("blank")
                    }
                    var input_id = textBlock.attr("id").replace("_display_value", "")
                    var input_update = $('input[id="' + input_id + '"]');
                    var form = $('form[action="/send_email_form"]')
                    input_update.val(textBox.val())
                }
            };
        };

        var $edit = $('.makeEditable').editable();
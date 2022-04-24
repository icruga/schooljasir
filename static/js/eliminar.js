$(document).ready(function()
{
    $('.dltBtn').click(function(e){
    e.preventDefault();
    var id = $(this).attr('data-id');
    var parent = $(this).parent("td").parent("tr");
    bootbox.dialog(
        {
            message: "¿Estás seguro de eliminar el registro?",
            title: "<i class='fa fa-trash-o'></i> ¡Atención!",
            buttons: {
                cancel: {
                    label: "No",
                    className: "btn-success",
                    callback: function() {
                    $('.bootbox').modal('hide');
                                         }
                        },
                confirm: {
                    label: "Eliminar",
                    className: "btn-danger",
                    callback: function() {
                    $.ajax({
                    url: '/eliminar_persona',
                    data: {id:id}
                            })
                //Si todo ha ido bien...
                .done(function(response){
                parent.fadeOut('slow'); //Borra la fila afectada
                })
                .fail(function(){
                    bootbox.alert('Algo ha ido mal. No se ha podido completar la acción.');
                    })
                                        }
                            }
                }
            });
            });





//clic cuando ul usuario de actulizar
//boton alerta
     $('.actualizar').click(function(e){
          var id = $(this).attr('data-id');

         bootbox.confirm({
    message: "¿Desea modificar el usuario?",
    buttons: {
        confirm: {
            label: 'Aceptar',
            className: 'btn-success'
        },
        cancel: {
            label: 'No',
            className: 'btn-danger'
        }
    },
  callback: function (result) {
        window.location.href = "/actualizar_persona/"+id;
        console.log('This was logged in the callback: ' + result);
        console.log("id es:"+id)
    }
});
     });

});
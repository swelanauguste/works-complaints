$(document).ready(function () {
var commonClasses = 'form-control form-control-sm rounded-2 border border-secondary'
$('button[type="submit"]').addClass('btn btn-dark rounded-2 px-5');
$('input[type="text"]').addClass(commonClasses);
$('input[type="password"]').addClass(commonClasses, 'rounded-2');
$('input[type="email"]').addClass(commonClasses);
$('input[type="file"]').addClass('rounded-2');
$('select').addClass(commonClasses);
$('textarea').addClass(commonClasses);
$('a').addClass('text-dark');
$('.page').addClass('badge text-bg-dark text-white text-decoration-none');
$('.link').addClass('text-decoration-none');
$('#filter-zones').select2();
$('#id_investigators').select2();
$('#id_zone').select2();
$('#id_engineer').select2();
$('#id_engineering_assistant').select2();
$('#id_technician').select2();
$('#id_cc').select2();
$('#id_programme').select2();
});
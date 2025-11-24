--En auth crean tres usuarios:
/* (basta con crear dos en realidad pero mejor tener otro por si acaso, el normal y el 3 para que no tengan que cambiar nada en el postman)
student@example.com
student2@example.com                      todos con contraseña: ChangeMe123!
student3@example.com

guardan el uuid y lo colocan en el código de abajo según se especifica por estudiante, pueden omitir el student 2
solo se piden dos usuarios para pruebas, vamos a usar el normal y el student3

*/


insert into public.user_allowed_country (user_id, country_code) values
('7052a784-95ed-42cb-b0eb-e2127df8d539', 'CR'), --student3@example.com
('edaea588-85d5-4891-ace7-5fe847780765', 'FR'), --student@example.com
('c2c6ecf6-f9b6-43ed-9545-ede583390220', 'ES'); --student2@example.com

insert into public.user_allowed_category (user_id, category_id) values
('7052a784-95ed-42cb-b0eb-e2127df8d539', (select id from public.categories where name ='Electronics')), --student3@example.com
('edaea588-85d5-4891-ace7-5fe847780765', (select id from public.categories where name = 'Beauty')), --student@example.com
('c2c6ecf6-f9b6-43ed-9545-ede583390220', (select id from public.categories where name = 'Food')), --student2@example.com
('c2c6ecf6-f9b6-43ed-9545-ede583390220', (select id from public.categories where name ='Clothing')); --student2@example.com



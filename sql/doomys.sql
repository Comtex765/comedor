INSERT INTO public.meal_time(id_meal_time, meal_time, init_hour, end_hour)
	VALUES 
      (1, 'Desayuno','06:30:00','11:45:00'),
      (2, 'Almuerzo','12:00:00','15:00:00'),
      (3, 'Merienda','18:00:00','21:00:00');

INSERT INTO public.menu_type(id_menu_type, menu_type)
	VALUES 
      (1, 'Normal'),
      (2, 'Vegetariano'),
      (3, 'Vegano'),
      (4, 'Alergias');
   
INSERT INTO public.user_type(id_user_type, description, percent_discount)
	VALUES 
      (0, 'Administrador', 0),
      (1, 'Estudiante',	25),
      (2, 'Profesor', 10),
      (3, 'Personal', 15);

INSERT INTO public.reserve_status(id_status, reserve_status)
	VALUES 
      (1, 'Próxima'),
      (2, 'Cancelada'),
      (3, 'Realizada');

INSERT INTO public.users(id_user, id_user_type, user_name, user_last_name, email, hash_password, cellphone, balance, created_date, cedula)
	VALUES 
      (1, 1 , 'Fernando' , 'Novillo', 'ferchon123443@gmail.com', 'Fernando12', '0994637276', 0, LOCALTIMESTAMP, '0604401919');
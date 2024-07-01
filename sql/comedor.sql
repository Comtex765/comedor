
/*==============================================================*/
/* Table: card                                                  */
/*==============================================================*/
create table card (
   id_card              SERIAL               not null,
   id_user              INT4                 null,
   card_number          VARCHAR(100)         null,
   exp_month            VARCHAR(100)         null,
   exp_year             VARCHAR(100)         null,
   constraint PK_CARD primary key (id_card)
);

/*==============================================================*/
/* Table: dining_reservation                                    */
/*==============================================================*/
create table dining_reservation (
   id_reservation       SERIAL               not null,
   id_menu              INT4                 not null,
   id_user              INT4                 not null,
   id_status            INT4                 null,
   reservation_date     DATE                 null,
   reservation_hour     TIME                 null,
   created_date         timestamp            null,
   total_cost           DECIMAL(5,2)         null,
   constraint PK_DINING_RESERVATION primary key (id_reservation, id_menu, id_user)
);

/*==============================================================*/
/* Table: meal_time                                             */
/*==============================================================*/
create table meal_time (
   id_meal_time         SERIAL               not null,
   meal_time            VARCHAR(50)          null,
   init_hour            TIME                 null,
   end_hour             TIME                 null,
   constraint PK_MEAL_TIME primary key (id_meal_time)
);

/*==============================================================*/
/* Table: menu                                                  */
/*==============================================================*/
create table menu (
   id_menu              SERIAL               not null,
   id_menu_type         INT4                 null,
   id_meal_time         INT4                 null,
   menu_title           VARCHAR(50)          null,
   menu_description     TEXT                 null,
   menu_date            DATE                 null,
   price                DECIMAL(5,2)         null,
   constraint PK_MENU primary key (id_menu)
);

/*==============================================================*/
/* Table: menu_type                                             */
/*==============================================================*/
create table menu_type (
   id_menu_type         SERIAL               not null,
   menu_type            VARCHAR(50)          null,
   constraint PK_MENU_TYPE primary key (id_menu_type)
);

/*==============================================================*/
/* Table: reserve_status                                        */
/*==============================================================*/
create table reserve_status (
   id_status            SERIAL               not null,
   reserve_status       VARCHAR(50)          null,
   constraint PK_RESERVE_STATUS primary key (id_status)
);

/*==============================================================*/
/* Table: suggests                                              */
/*==============================================================*/
create table suggests (
   id_suggest           SERIAL               not null,
   id_user              INT4                 null,
   suggestion           TEXT                 null,
   created_cate         DATE                 null,
   constraint PK_SUGGESTS primary key (id_suggest)
);

/*==============================================================*/
/* Table: user_type                                             */
/*==============================================================*/
create table user_type (
   id_user_type         SERIAL               not null,
   description          VARCHAR(100)         null,
   percent_discount     INT4                 null,
   constraint PK_USER_TYPE primary key (id_user_type)
);

/*==============================================================*/
/* Table: users                                                 */
/*==============================================================*/
create table users (
   id_user              SERIAL               not null,
   id_user_type         INT4                 null,
   user_name            VARCHAR(100)         null,
   user_last_name       VARCHAR(100)         null,
   email                VARCHAR(100)         unique null,
   hash_password        VARCHAR(200)         null,
   cellphone            CHAR(10)             unique null,
   balance              DECIMAL(10,2)                null,
   created_date         timestamp            null,
   constraint PK_USERS primary key (id_user)
);

alter table card
   add constraint FK_CARD_REFERENCE_USERS foreign key (id_user)
      references users (id_user)
      on delete restrict on update restrict;

alter table dining_reservation
   add constraint FK_DINING_R_REFERENCE_MENU foreign key (id_menu)
      references menu (id_menu)
      on delete restrict on update restrict;

alter table dining_reservation
   add constraint FK_DINING_R_REFERENCE_USERS foreign key (id_user)
      references users (id_user)
      on delete restrict on update restrict;

alter table dining_reservation
   add constraint FK_DINING_R_REFERENCE_RESERVE_ foreign key (id_status)
      references reserve_status (id_status)
      on delete restrict on update restrict;

alter table menu
   add constraint FK_MENU_REFERENCE_MENU_TYP foreign key (id_menu_type)
      references menu_type (id_menu_type)
      on delete restrict on update restrict;

alter table menu
   add constraint FK_MENU_REFERENCE_MEAL_TIM foreign key (id_meal_time)
      references meal_time (id_meal_time)
      on delete restrict on update restrict;

alter table suggests
   add constraint FK_SUGGESTS_REFERENCE_USERS foreign key (id_user)
      references users (id_user)
      on delete restrict on update restrict;

alter table users
   add constraint FK_USERS_REFERENCE_USER_TYP foreign key (id_user_type)
      references user_type (id_user_type)
      on delete restrict on update restrict;


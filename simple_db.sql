--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: department; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE department (
    id integer NOT NULL,
    code text DEFAULT ''::text NOT NULL,
    name text DEFAULT ''::text NOT NULL,
    parent_id integer DEFAULT 0,
    sort integer DEFAULT 0,
    level integer DEFAULT 0,
    is_leaf boolean DEFAULT false,
    expanded boolean DEFAULT false
);


ALTER TABLE department OWNER TO postgres;

--
-- Name: TABLE department; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE department IS '部门管理表';


--
-- Name: COLUMN department.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN department.id IS '主键Id';


--
-- Name: COLUMN department.code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN department.code IS '部门ID，内容为010101，即每低一级部门，编码增加两位小数';


--
-- Name: COLUMN department.name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN department.name IS '部门名称';


--
-- Name: COLUMN department.parent_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN department.parent_id IS '父ID';


--
-- Name: COLUMN department.sort; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN department.sort IS '排序';


--
-- Name: COLUMN department.level; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN department.level IS '树列表深度级别，即当前数据在哪一级';


--
-- Name: COLUMN department.is_leaf; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN department.is_leaf IS '是否最终节点';


--
-- Name: COLUMN department.expanded; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN department.expanded IS '此节点是否展开，后台菜单列表js要用到，不用进行编辑';


--
-- Name: department_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE department_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE department_id_seq OWNER TO postgres;

--
-- Name: department_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE department_id_seq OWNED BY department.id;


--
-- Name: infomation; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE infomation (
    id integer NOT NULL,
    title text DEFAULT ''::text,
    front_cover_img text DEFAULT ''::text,
    content text DEFAULT ''::text,
    add_time timestamp(0) without time zone DEFAULT now() NOT NULL
);


ALTER TABLE infomation OWNER TO postgres;

--
-- Name: TABLE infomation; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE infomation IS '信息表';


--
-- Name: COLUMN infomation.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN infomation.id IS '主键Id';


--
-- Name: COLUMN infomation.title; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN infomation.title IS '标题';


--
-- Name: COLUMN infomation.front_cover_img; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN infomation.front_cover_img IS '封面图片地址（首页）';


--
-- Name: COLUMN infomation.content; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN infomation.content IS '内容';


--
-- Name: COLUMN infomation.add_time; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN infomation.add_time IS '添加时间';


--
-- Name: infomation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE infomation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE infomation_id_seq OWNER TO postgres;

--
-- Name: infomation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE infomation_id_seq OWNED BY infomation.id;


--
-- Name: manager; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE manager (
    id integer NOT NULL,
    login_name text DEFAULT ''::text NOT NULL,
    login_password text DEFAULT ''::text NOT NULL,
    login_key text DEFAULT ''::text,
    last_login_time timestamp(0) without time zone,
    last_login_ip text DEFAULT ''::text,
    login_count integer DEFAULT 0,
    create_time timestamp(0) without time zone DEFAULT now() NOT NULL,
    department_id integer DEFAULT 0,
    department_code text DEFAULT ''::text,
    department_name text DEFAULT ''::text,
    positions_id integer DEFAULT 0,
    positions_name text DEFAULT ''::text,
    is_work boolean DEFAULT false,
    is_enabled boolean DEFAULT false,
    name text DEFAULT ''::text NOT NULL,
    sex text DEFAULT ''::text,
    birthday date,
    mobile text DEFAULT ''::text,
    email text DEFAULT ''::text,
    remark text DEFAULT ''::text,
    manager_id integer DEFAULT 0,
    manager_name text DEFAULT ''::text
);


ALTER TABLE manager OWNER TO postgres;

--
-- Name: TABLE manager; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE manager IS '管理员管理表';


--
-- Name: COLUMN manager.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager.id IS '主键Id';


--
-- Name: COLUMN manager.login_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager.login_name IS '登陆账号';


--
-- Name: COLUMN manager.login_password; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager.login_password IS '登陆密码';


--
-- Name: COLUMN manager.login_key; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager.login_key IS '登录密钥';


--
-- Name: COLUMN manager.last_login_time; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager.last_login_time IS '最后登陆时间';


--
-- Name: COLUMN manager.last_login_ip; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager.last_login_ip IS '最后登陆IP';


--
-- Name: COLUMN manager.login_count; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager.login_count IS '登陆次数';


--
-- Name: COLUMN manager.create_time; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager.create_time IS '注册时间';


--
-- Name: COLUMN manager.department_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager.department_id IS '部门自编号Id，用户只能归属于一个部门';


--
-- Name: COLUMN manager.department_code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager.department_code IS '部门编号';


--
-- Name: COLUMN manager.department_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager.department_name IS '部门名称';


--
-- Name: COLUMN manager.positions_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager.positions_id IS '用户职位Id';


--
-- Name: COLUMN manager.positions_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager.positions_name IS '职位名称';


--
-- Name: COLUMN manager.is_work; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager.is_work IS '0=离职，1=就职';


--
-- Name: COLUMN manager.is_enabled; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager.is_enabled IS '账号是否启用，true=启用，false=禁用';


--
-- Name: COLUMN manager.name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager.name IS '用户中文名称';


--
-- Name: COLUMN manager.sex; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager.sex IS '性别（未知，男，女）';


--
-- Name: COLUMN manager.birthday; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager.birthday IS '出生日期';


--
-- Name: COLUMN manager.mobile; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager.mobile IS '手机号码';


--
-- Name: COLUMN manager.email; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager.email IS '个人--联系邮箱';


--
-- Name: COLUMN manager.remark; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager.remark IS '备注';


--
-- Name: COLUMN manager.manager_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager.manager_id IS '操作人员id';


--
-- Name: COLUMN manager.manager_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager.manager_name IS '操作人员姓名';


--
-- Name: manager_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE manager_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE manager_id_seq OWNER TO postgres;

--
-- Name: manager_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE manager_id_seq OWNED BY manager.id;


--
-- Name: manager_operation_log; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE manager_operation_log (
    id integer NOT NULL,
    ip text DEFAULT ''::text,
    remark text DEFAULT ''::text,
    manager_id integer DEFAULT 0,
    manager_name text DEFAULT ''::text,
    add_time timestamp(0) without time zone DEFAULT now() NOT NULL
);


ALTER TABLE manager_operation_log OWNER TO postgres;

--
-- Name: TABLE manager_operation_log; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE manager_operation_log IS '管理员操作日志表';


--
-- Name: COLUMN manager_operation_log.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager_operation_log.id IS '主键Id';


--
-- Name: COLUMN manager_operation_log.ip; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager_operation_log.ip IS '登陆IP';


--
-- Name: COLUMN manager_operation_log.remark; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager_operation_log.remark IS '操作内容';


--
-- Name: COLUMN manager_operation_log.manager_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager_operation_log.manager_id IS '操作人员id';


--
-- Name: COLUMN manager_operation_log.manager_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager_operation_log.manager_name IS '操作人员姓名';


--
-- Name: COLUMN manager_operation_log.add_time; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN manager_operation_log.add_time IS '添加时间';


--
-- Name: manager_operation_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE manager_operation_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE manager_operation_log_id_seq OWNER TO postgres;

--
-- Name: manager_operation_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE manager_operation_log_id_seq OWNED BY manager_operation_log.id;


--
-- Name: menu_info; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE menu_info (
    id integer NOT NULL,
    name text DEFAULT ''::text NOT NULL,
    icon text DEFAULT ''::text,
    page_url text DEFAULT ''::text,
    interface_url text DEFAULT ''::text,
    parent_id integer DEFAULT 0,
    sort integer DEFAULT 0,
    level integer DEFAULT 0,
    is_leaf boolean DEFAULT false,
    expanded boolean DEFAULT false,
    is_show boolean DEFAULT true,
    is_enabled boolean DEFAULT true
);


ALTER TABLE menu_info OWNER TO postgres;

--
-- Name: TABLE menu_info; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE menu_info IS '菜单表';


--
-- Name: COLUMN menu_info.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN menu_info.id IS '主键Id';


--
-- Name: COLUMN menu_info.name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN menu_info.name IS '菜单名称或各个页面功能名称';


--
-- Name: COLUMN menu_info.icon; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN menu_info.icon IS '菜单小图标（一级菜单需要设置，二级菜单不用）';


--
-- Name: COLUMN menu_info.page_url; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN menu_info.page_url IS '各页面URL（主菜单与分类菜单没有URL）';


--
-- Name: COLUMN menu_info.interface_url; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN menu_info.interface_url IS '各接口url';


--
-- Name: COLUMN menu_info.parent_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN menu_info.parent_id IS '父ID';


--
-- Name: COLUMN menu_info.sort; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN menu_info.sort IS '排序';


--
-- Name: COLUMN menu_info.level; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN menu_info.level IS '树列表深度级别，即当前数据在哪一级';


--
-- Name: COLUMN menu_info.is_leaf; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN menu_info.is_leaf IS '是否最终节点';


--
-- Name: COLUMN menu_info.expanded; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN menu_info.expanded IS '此节点是否展开，后台菜单列表js要用到，不用进行编辑';


--
-- Name: COLUMN menu_info.is_show; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN menu_info.is_show IS '该菜单是否在菜单栏显示，false=不显示，true=显示';


--
-- Name: COLUMN menu_info.is_enabled; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN menu_info.is_enabled IS '是否启用，true=启用，false=禁用';


--
-- Name: menu_info_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE menu_info_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE menu_info_id_seq OWNER TO postgres;

--
-- Name: menu_info_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE menu_info_id_seq OWNED BY menu_info.id;


--
-- Name: positions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE positions (
    id integer NOT NULL,
    name text DEFAULT ''::text,
    department_id integer DEFAULT 0 NOT NULL,
    department_code text DEFAULT ''::text NOT NULL,
    department_name text DEFAULT ''::text,
    page_power text DEFAULT ''::text
);


ALTER TABLE positions OWNER TO postgres;

--
-- Name: TABLE positions; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE positions IS '职位管理表';


--
-- Name: COLUMN positions.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN positions.id IS '主键Id';


--
-- Name: COLUMN positions.name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN positions.name IS '职位名称';


--
-- Name: COLUMN positions.department_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN positions.department_id IS '部门自编号ID';


--
-- Name: COLUMN positions.department_code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN positions.department_code IS '部门编号';


--
-- Name: COLUMN positions.department_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN positions.department_name IS '部门名称';


--
-- Name: COLUMN positions.page_power; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN positions.page_power IS '菜单操作权限，有操作权限的菜单ID列表：,1,2,3,4,5,';


--
-- Name: positions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE positions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE positions_id_seq OWNER TO postgres;

--
-- Name: positions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE positions_id_seq OWNED BY positions.id;


--
-- Name: product; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE product (
    id integer NOT NULL,
    name text DEFAULT ''::text NOT NULL,
    code text DEFAULT ''::text,
    product_class_id integer DEFAULT 0,
    standard text DEFAULT ''::text,
    quality_guarantee_period text DEFAULT ''::text,
    place_of_origin text DEFAULT ''::text,
    front_cover_img text DEFAULT ''::text,
    content text DEFAULT ''::text,
    is_enable integer DEFAULT 0,
    add_time timestamp(0) without time zone DEFAULT now() NOT NULL
);


ALTER TABLE product OWNER TO postgres;

--
-- Name: TABLE product; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE product IS '产品信息';


--
-- Name: COLUMN product.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN product.id IS '主键Id';


--
-- Name: COLUMN product.name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN product.name IS '菜单名称或各个页面功能名称';


--
-- Name: COLUMN product.code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN product.code IS '产品编码';


--
-- Name: COLUMN product.product_class_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN product.product_class_id IS '所属产品分类';


--
-- Name: COLUMN product.standard; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN product.standard IS '产品规格';


--
-- Name: COLUMN product.quality_guarantee_period; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN product.quality_guarantee_period IS '保质期';


--
-- Name: COLUMN product.place_of_origin; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN product.place_of_origin IS '产地';


--
-- Name: COLUMN product.front_cover_img; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN product.front_cover_img IS '封面图片地址（展示图片）';


--
-- Name: COLUMN product.content; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN product.content IS '产品描述';


--
-- Name: COLUMN product.is_enable; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN product.is_enable IS '是否启用，1=true(启用)，0=false（禁用）';


--
-- Name: COLUMN product.add_time; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN product.add_time IS '添加时间';


--
-- Name: product_class; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE product_class (
    id integer NOT NULL,
    name text DEFAULT ''::text NOT NULL,
    is_enable integer DEFAULT 0,
    add_time timestamp(0) without time zone DEFAULT now() NOT NULL
);


ALTER TABLE product_class OWNER TO postgres;

--
-- Name: TABLE product_class; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE product_class IS '产品分类';


--
-- Name: COLUMN product_class.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN product_class.id IS '主键Id';


--
-- Name: COLUMN product_class.name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN product_class.name IS '菜单名称或各个页面功能名称';


--
-- Name: COLUMN product_class.is_enable; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN product_class.is_enable IS '是否启用，1=true(启用)，0=false（禁用）';


--
-- Name: COLUMN product_class.add_time; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN product_class.add_time IS '添加时间';


--
-- Name: product_class_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE product_class_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE product_class_id_seq OWNER TO postgres;

--
-- Name: product_class_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE product_class_id_seq OWNED BY product_class.id;


--
-- Name: product_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE product_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE product_id_seq OWNER TO postgres;

--
-- Name: product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE product_id_seq OWNED BY product.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY department ALTER COLUMN id SET DEFAULT nextval('department_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY infomation ALTER COLUMN id SET DEFAULT nextval('infomation_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY manager ALTER COLUMN id SET DEFAULT nextval('manager_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY manager_operation_log ALTER COLUMN id SET DEFAULT nextval('manager_operation_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY menu_info ALTER COLUMN id SET DEFAULT nextval('menu_info_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY positions ALTER COLUMN id SET DEFAULT nextval('positions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY product ALTER COLUMN id SET DEFAULT nextval('product_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY product_class ALTER COLUMN id SET DEFAULT nextval('product_class_id_seq'::regclass);


--
-- Data for Name: department; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY department (id, code, name, parent_id, sort, level, is_leaf, expanded) FROM stdin;
2	0101	软件开发部	1	1	1	t	f
3	0102	行政部	1	2	1	t	f
4	0103	财务部	1	2	1	t	f
1	01	xx公司	0	1	0	f	f
\.


--
-- Name: department_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('department_id_seq', 4, true);


--
-- Data for Name: infomation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY infomation (id, title, front_cover_img, content, add_time) FROM stdin;
2	联系我们		<p><span>    地址：广州市天河区黄浦大道XX号</span><br><span>    邮编： 510000</span><br><span>    电话： 4008-0000-00 020-00000000</span><br><span>    Email：xxxx@xxx.com</span></p><p><span><img src="http://api.map.baidu.com/staticimage?center=113.271429,23.135336&amp;zoom=13&amp;width=530&amp;height=340&amp;markers=113.271429,23.135336" width="530" height="340"></span></p>	2018-08-30 15:25:19
1	公司介绍	http://localhost:81/upload/20180830/20180830162343CYK2U.gif	<p>XXXX物科技有限公xxxx集团，成立于2011年3月，注册资本1000万元，是XXXX开发销售的公司，主要XXX产品的销售。 旗下的XXX品牌源自XXX先生创立XXX，经过一百多年的发展，现已成为最具规模化，现代化，专业化的XXXX生产企业之一。 公司特与XXXX超市股份有限公司、XXXX集团股份有限公司等合作，在XX省多个城市100多家门店进行销售。</p><p>    公司本着“客户至上，质量为本”的原则，建立健全了严苛的质量标准检验体系，除了通过国家食品认证体系之外，还委托国家轻工业食品质量监督检测XX站特别做了XXX检测，XXX检测，以远远低于国家标准的检测结果确保XX品质。</p>	2018-08-30 15:25:10
\.


--
-- Name: infomation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('infomation_id_seq', 2, true);


--
-- Data for Name: manager; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY manager (id, login_name, login_password, login_key, last_login_time, last_login_ip, login_count, create_time, department_id, department_code, department_name, positions_id, positions_name, is_work, is_enabled, name, sex, birthday, mobile, email, remark, manager_id, manager_name) FROM stdin;
1	admin	e10adc3949ba59abbe56e057f20f883e		2018-09-14 12:05:32	127.0.0.1	10	2018-08-23 15:58:52	2	0101	软件开发部	1	软件开发人员	t	t	admin	男	\N	13900000000			0	
\.


--
-- Name: manager_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('manager_id_seq', 1, true);


--
-- Data for Name: manager_operation_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY manager_operation_log (id, ip, remark, manager_id, manager_name, add_time) FROM stdin;
1	127.0.0.1	用户进行访问[菜单管理列表]操作	1	admin	2018-09-14 10:19:32
2	127.0.0.1	用户进行访问[菜单管理添加]操作	1	admin	2018-09-14 10:19:35
3	127.0.0.1	用户进行访问[菜单管理编辑]操作	1	admin	2018-09-14 10:19:35
4	127.0.0.1	用户进行[菜单管理编辑]操作	1	admin	2018-09-14 10:19:38
5	127.0.0.1	用户进行访问[菜单管理列表]操作	1	admin	2018-09-14 10:19:40
6	127.0.0.1	用户进行访问[菜单管理添加]操作	1	admin	2018-09-14 10:22:06
7	127.0.0.1	用户进行访问[菜单管理编辑]操作	1	admin	2018-09-14 10:22:07
8	127.0.0.1	用户进行访问[菜单管理列表]操作	1	admin	2018-09-14 10:22:12
9	127.0.0.1	用户进行访问[菜单管理列表]操作	1	admin	2018-09-14 10:22:49
10	127.0.0.1	用户进行[菜单管理编辑]操作	1	admin	2018-09-14 10:22:53
11	127.0.0.1	用户进行访问[菜单管理列表]操作	1	admin	2018-09-14 10:22:55
12	127.0.0.1	用户[信息管理公司介绍]操作	1	admin	2018-09-14 10:26:36
13	127.0.0.1	用户进行[信息管理公司介绍]操作	1	admin	2018-09-14 10:27:22
14	127.0.0.1	用户访问[http://localhost/api/product_class/]接口地址时，检测没有操作权限	1	admin	2018-09-14 10:28:15
15	127.0.0.1	用户访问[菜单管理列表]操作	1	admin	2018-09-14 10:30:00
16	127.0.0.1	用户访问[菜单管理列表]操作	1	admin	2018-09-14 10:30:03
17	127.0.0.1	用户访问[菜单管理列表]操作	1	admin	2018-09-14 10:30:05
18	127.0.0.1	用户访问[菜单管理列表]操作	1	admin	2018-09-14 10:30:07
19	127.0.0.1	用户访问[http://localhost/api/product_class/]接口地址时，检测没有操作权限	1	admin	2018-09-14 10:30:22
20	127.0.0.1	用户进行[菜单管理编辑]操作	1	admin	2018-09-14 10:31:48
21	127.0.0.1	用户访问[菜单管理列表]操作	1	admin	2018-09-14 10:31:50
22	127.0.0.1	用户访问[菜单管理列表]操作	1	admin	2018-09-14 10:31:52
23	127.0.0.1	用户访问[菜单管理列表]操作	1	admin	2018-09-14 10:31:54
24	127.0.0.1	用户进行[菜单管理编辑]操作	1	admin	2018-09-14 10:32:00
25	127.0.0.1	用户访问[菜单管理列表]操作	1	admin	2018-09-14 10:32:02
26	127.0.0.1	用户进行[产品分类管理添加]操作	1	admin	2018-09-14 10:32:05
27	127.0.0.1	用户进行[产品分类管理添加]操作	1	admin	2018-09-14 10:32:43
28	127.0.0.1	用户进行[产品分类管理删除]操作	1	admin	2018-09-14 10:32:48
29	127.0.0.1	用户进行[产品列表添加]操作	1	admin	2018-09-14 10:33:32
30	127.0.0.1	用户进行[产品列表编辑]操作	1	admin	2018-09-14 10:33:49
31	127.0.0.1	用户进行[产品列表编辑]操作	1	admin	2018-09-14 10:33:49
32	127.0.0.1	用户进行[产品列表删除]操作	1	admin	2018-09-14 10:34:00
33	127.0.0.1	用户进行[产品添加]操作	1	admin	2018-09-14 10:37:47
34	127.0.0.1	用户进行[产品删除]操作	1	admin	2018-09-14 10:37:53
35	127.0.0.1	【admin】退出登录	1	admin	2018-09-14 12:03:23
36	127.0.0.1	【admin】登陆成功	1	admin	2018-09-14 12:05:32
37	127.0.0.1	用户访问[主界面]操作	1	admin	2018-09-14 12:05:33
38	127.0.0.1	用户访问[菜单列表]操作	1	admin	2018-09-14 14:21:42
39	127.0.0.1	用户访问[菜单列表]操作	1	admin	2018-09-14 14:21:45
40	127.0.0.1	用户进行[菜单添加]操作	1	admin	2018-09-14 14:22:26
41	127.0.0.1	用户访问[菜单列表]操作	1	admin	2018-09-14 14:22:28
42	127.0.0.1	用户进行[菜单添加]操作	1	admin	2018-09-14 14:22:50
43	127.0.0.1	用户访问[菜单列表]操作	1	admin	2018-09-14 14:22:52
44	127.0.0.1	用户访问[菜单列表]操作	1	admin	2018-09-14 14:22:53
45	127.0.0.1	用户进行[菜单编辑]操作	1	admin	2018-09-14 14:22:58
46	127.0.0.1	用户访问[菜单列表]操作	1	admin	2018-09-14 14:23:01
47	127.0.0.1	用户访问[菜单列表]操作	1	admin	2018-09-14 14:23:04
48	127.0.0.1	用户进行[菜单编辑]操作	1	admin	2018-09-14 14:23:19
49	127.0.0.1	用户访问[菜单列表]操作	1	admin	2018-09-14 14:23:21
50	127.0.0.1	用户进行[菜单添加]操作	1	admin	2018-09-14 14:23:39
51	127.0.0.1	用户进行[菜单添加]操作	1	admin	2018-09-14 14:23:45
52	127.0.0.1	用户进行[菜单添加]操作	1	admin	2018-09-14 14:23:50
53	127.0.0.1	用户访问[菜单列表]操作	1	admin	2018-09-14 14:23:52
54	127.0.0.1	用户访问[菜单列表]操作	1	admin	2018-09-14 14:23:53
55	127.0.0.1	用户进行[菜单编辑]操作	1	admin	2018-09-14 14:24:10
56	127.0.0.1	用户访问[菜单列表]操作	1	admin	2018-09-14 14:24:12
57	127.0.0.1	用户进行[菜单添加]操作	1	admin	2018-09-14 14:24:35
58	127.0.0.1	用户访问[菜单列表]操作	1	admin	2018-09-14 14:24:37
59	127.0.0.1	用户访问[菜单列表]操作	1	admin	2018-09-14 14:24:39
60	127.0.0.1	用户访问[菜单列表]操作	1	admin	2018-09-14 14:24:41
61	127.0.0.1	用户访问[菜单列表]操作	1	admin	2018-09-14 14:24:43
62	127.0.0.1	用户访问[职位列表]操作	1	admin	2018-09-14 14:24:54
63	127.0.0.1	用户访问[职位列表]操作	1	admin	2018-09-14 14:24:54
64	127.0.0.1	用户访问[职位列表]操作	1	admin	2018-09-14 14:24:56
65	127.0.0.1	用户访问[职位列表]操作	1	admin	2018-09-14 14:24:57
66	127.0.0.1	用户进行[职位编辑]操作	1	admin	2018-09-14 14:25:09
67	127.0.0.1	用户访问[职位列表]操作	1	admin	2018-09-14 14:25:10
68	127.0.0.1	用户访问[主界面]操作	1	admin	2018-09-14 14:25:11
69	127.0.0.1	用户访问[员操作日志列表]操作	1	admin	2018-09-14 14:26:31
70	127.0.0.1	用户访问[员操作日志列表]操作	1	admin	2018-09-14 14:26:42
71	127.0.0.1	用户访问[员操作日志列表]操作	1	admin	2018-09-14 14:26:54
72	127.0.0.1	用户访问[员操作日志列表]操作	1	admin	2018-09-14 14:27:03
73	127.0.0.1	用户访问[员操作日志列表]操作	1	admin	2018-09-14 14:27:06
74	127.0.0.1	用户访问[员操作日志列表]操作	1	admin	2018-09-14 14:27:11
75	127.0.0.1	用户访问[员操作日志列表]操作	1	admin	2018-09-14 14:27:19
76	127.0.0.1	用户访问[员操作日志列表]操作	1	admin	2018-09-14 14:27:23
77	127.0.0.1	用户访问[员操作日志列表]操作	1	admin	2018-09-14 14:27:28
78	127.0.0.1	用户访问[员操作日志列表]操作	1	admin	2018-09-14 14:27:38
79	127.0.0.1	用户访问[员操作日志列表]操作	1	admin	2018-09-14 14:29:24
80	127.0.0.1	用户访问[员操作日志列表]操作	1	admin	2018-09-14 14:29:41
81	127.0.0.1	用户访问[员操作日志列表]操作	1	admin	2018-09-14 14:32:04
82	127.0.0.1	用户访问[员操作日志列表]操作	1	admin	2018-09-14 14:32:37
83	127.0.0.1	用户访问[员操作日志列表]操作	1	admin	2018-09-14 14:32:40
84	127.0.0.1	用户访问[员操作日志列表]操作	1	admin	2018-09-14 14:32:42
\.


--
-- Name: manager_operation_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('manager_operation_log_id_seq', 84, true);


--
-- Data for Name: menu_info; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY menu_info (id, name, icon, page_url, interface_url, parent_id, sort, level, is_leaf, expanded, is_show, is_enabled) FROM stdin;
2	菜单管理		menu_info.html		1	1	1	f	f	t	t
3	列表		menu_info.html	get(/api/system/menu_info/)	2	1	2	t	f	f	t
5	编辑		menu_info_edit.html	get(/api/system/menu_info/tree/),get(/api/system/menu_info/<id:int>/),put(/api/system/menu_info/<id:int>/)	2	3	2	t	f	f	t
4	添加		menu_info_edit.html	get(/api/system/menu_info/tree/),post(/api/system/menu_info/)	2	2	2	t	f	f	t
7	部门管理		department.html		1	2	1	f	f	t	t
8	列表		department.html	get(/api/system/department/)	7	1	2	t	f	f	t
40	列表		manager_operation_log.html	get(/api/system/manager_operation_log/)	39	1	2	t	f	f	t
6	删除		menu_info.html	delete(/api/system/menu_info/<id:int>/)	2	4	2	t	f	f	t
9	添加		department_edit.html	get(/api/system/department/tree/),post(/api/system/department/)	7	2	2	t	f	f	t
10	编辑		department_edit.html	get(/api/system/department/tree/),get(/api/system/department/<id:int>/),put(/api/system/department/<id:int>/)	7	3	2	t	f	f	t
11	删除		department.html	delete(/api/system/department/<id:int>/)	7	4	2	t	f	f	t
13	产品分类管理		products_class.html		12	1	1	f	f	t	t
14	列表		products_class.html	get(/api/product_class/)	13	1	2	t	f	f	t
17	删除		products_class.html	delete(/api/product_class/<id:int>/)	13	4	2	t	f	f	t
18	产品列表		products_list.html		12	2	1	f	f	t	t
20	添加		products_edit.html	get(/api/product_class/),post(/api/product/)	18	2	2	t	f	f	t
21	编辑		products_edit.html	get(/api/product_class/),get(/api/product/<id:int>/),put(/api/product/<id:int>/),post(/api/files/)	18	3	2	t	f	f	t
22	删除		products_list.html	delete(/api/product/<id:int>/)	18	4	2	t	f	f	t
19	列表		products_list.html	get(/api/product_class/),get(/api/product/)	18	1	2	t	f	f	t
26	职位管理		positions.html		1	3	1	f	f	t	t
31	管理员管理		manager.html		1	4	1	f	f	t	t
32	列表		manager.html	get(/api/system/manager/)	31	1	2	t	f	f	t
33	添加		manager_edit.html	post(/api/system/manager/),get(/api/system/department/tree/),get(/api/system/positions/)	31	2	2	t	f	f	t
34	编辑		manager_edit.html	get(/api/system/manager/<id:int>/),put(/api/system/manager/<id:int>/),get(/api/system/department/tree/),get(/api/system/positions/)	31	3	2	t	f	f	t
35	删除		manager.html	delete(/api/system/manager/<id:int>/)	31	4	2	t	f	f	t
36	离职		manager.html	put(/api/system/manager/<id:int>/dimission/)	31	5	2	t	f	f	t
37	复职		manager.html	put(/api/system/manager/<id:int>/reinstated/)	31	6	2	t	f	f	t
38	主界面		main.html	get(/api/main/menu_info/)	0	1	0	t	f	f	t
12	产品管理	&#xe6b5;			0	10	0	f	f	t	t
27	列表		positions.html	get(/api/system/positions/),get(/api/system/department/),	26	1	2	t	f	f	t
39	管理员操作日志		manager_operation_log.html		1	5	1	f	f	t	t
28	添加		positions_edit.html	get(/api/system/menu_info/positions/<id:int>/),post(/api/system/positions/)	26	2	2	t	f	f	t
29	编辑		positions_edit.html	get(/api/system/menu_info/positions/<id:int>/),get(/api/system/positions/<id:int>/),put(/api/system/positions/<id:int>/)	26	3	2	t	f	f	t
30	删除		positions.html	delete(/api/system/positions/<id:int>/)	26	4	2	t	f	f	t
1	系统管理	&#xe62e;			0	2	0	f	f	t	t
23	信息管理	&#xe616;			0	20	0	f	f	t	t
15	添加		product_class_edit.html	post(/api/product_class/)	13	2	2	t	f	f	t
16	编辑		product_class_edit.html	get(/api/product_class/<id:int>/),put(/api/product_class/<id:int>/)	13	3	2	t	f	f	t
24	公司介绍		about_edit.html		23	1	1	f	f	t	t
41	编辑		about_edit.html	get(/api/about/),put(/api/about/)	24	1	2	t	f	f	t
25	联系我们		contact_us_edit.html		23	2	1	f	f	t	t
42	编辑		contact_us_edit.html	get(/api/contact_us/),put(/api/contact_us/)	25	1	2	t	f	f	t
\.


--
-- Name: menu_info_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('menu_info_id_seq', 42, true);


--
-- Data for Name: positions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY positions (id, name, department_id, department_code, department_name, page_power) FROM stdin;
1	软件开发人员	2	0101	软件开发部	,38,23,25,42,24,41,12,18,22,21,20,19,13,17,16,15,14,1,39,40,31,37,36,35,34,33,32,26,30,29,28,27,7,11,10,9,8,2,6,5,4,3,
\.


--
-- Name: positions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('positions_id_seq', 3, true);


--
-- Data for Name: product; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY product (id, name, code, product_class_id, standard, quality_guarantee_period, place_of_origin, front_cover_img, content, is_enable, add_time) FROM stdin;
15	葱油饼	201808031245678	1	200g	1年	广东深圳	/upload/20180830/20180830162650s1Uzi.png	<p>好吃</p>	1	2018-08-03 16:51:03
14	苏打饼	201807251234568	1	100g	1年	广东深圳	/upload/20180830/20180830162810cJQfu.png	<p>味道不错</p>	1	2018-08-03 00:14:14
7	入口即化威化饼	201807251234568	2	150g	1年	广东深圳	http://localhost:81/upload/20180830/20180830162856nPjF0.png	<p>赞</p>	1	2018-07-25 23:16:25
2	香橙味威化饼	20180212321211	2	500g	1年	广东广州	/upload/20180830/20180830163135Dmh9e.png	<p>产品详情</p>	1	2018-07-25 23:10:04
\.


--
-- Data for Name: product_class; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY product_class (id, name, is_enable, add_time) FROM stdin;
2	威化饼	1	2018-08-30 16:24:46
1	饼干	1	2018-08-17 16:14:54
3	果冻	1	2018-09-14 10:32:05
\.


--
-- Name: product_class_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('product_class_id_seq', 4, true);


--
-- Name: product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('product_id_seq', 17, true);


--
-- Name: department_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY department
    ADD CONSTRAINT department_pkey PRIMARY KEY (id);


--
-- Name: infomation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY infomation
    ADD CONSTRAINT infomation_pkey PRIMARY KEY (id);


--
-- Name: manager_operation_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY manager_operation_log
    ADD CONSTRAINT manager_operation_log_pkey PRIMARY KEY (id);


--
-- Name: manager_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY manager
    ADD CONSTRAINT manager_pkey PRIMARY KEY (id);


--
-- Name: menu_info_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY menu_info
    ADD CONSTRAINT menu_info_pkey PRIMARY KEY (id);


--
-- Name: positions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY positions
    ADD CONSTRAINT positions_pkey PRIMARY KEY (id);


--
-- Name: product_class_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY product_class
    ADD CONSTRAINT product_class_pkey PRIMARY KEY (id);


--
-- Name: product_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY product
    ADD CONSTRAINT product_pkey PRIMARY KEY (id);


--
-- Name: department_code_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX department_code_idx ON department USING btree (code);


--
-- Name: department_sort_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX department_sort_idx ON department USING btree (sort);


--
-- Name: manager_department_code_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX manager_department_code_idx ON manager USING btree (department_code);


--
-- Name: manager_department_id_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX manager_department_id_idx ON manager USING btree (department_id);


--
-- Name: manager_is_enabled_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX manager_is_enabled_idx ON manager USING btree (is_enabled);


--
-- Name: manager_is_work_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX manager_is_work_idx ON manager USING btree (is_work);


--
-- Name: manager_last_login_time_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX manager_last_login_time_idx ON manager USING btree (last_login_time);


--
-- Name: manager_login_name_idx1; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX manager_login_name_idx1 ON manager USING btree (login_name);


--
-- Name: manager_manager_id_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX manager_manager_id_idx ON manager USING btree (manager_id);


--
-- Name: manager_manager_name_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX manager_manager_name_idx ON manager USING btree (manager_name);


--
-- Name: manager_name_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX manager_name_idx ON manager USING btree (name);


--
-- Name: manager_operation_log_add_time_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX manager_operation_log_add_time_idx ON manager_operation_log USING btree (add_time);


--
-- Name: manager_operation_log_manager_id_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX manager_operation_log_manager_id_idx ON manager_operation_log USING btree (manager_id);


--
-- Name: manager_operation_log_manager_name_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX manager_operation_log_manager_name_idx ON manager_operation_log USING btree (manager_name);


--
-- Name: manager_positions_id_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX manager_positions_id_idx ON manager USING btree (positions_id);


--
-- Name: menu_info_is_show_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX menu_info_is_show_idx ON menu_info USING btree (is_show);


--
-- Name: menu_info_sort_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX menu_info_sort_idx ON menu_info USING btree (sort);


--
-- Name: positions_department_code_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX positions_department_code_idx ON positions USING btree (department_code);


--
-- Name: positions_department_id_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX positions_department_id_idx ON positions USING btree (department_id);


--
-- Name: positions_name_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX positions_name_idx ON positions USING btree (name);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--


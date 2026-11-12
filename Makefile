MODULE_big = data_encryption
OBJS = data_encryption.o
VPATH = SOURCES/data_encryption/tdeforpg

EXTENSION = tdeforpg
DATA_built = tdeforpg--1.0.sql
PGFILEDESC = "tdeforpg - Transparent Data Encryption for PostgreSQL Free Edition"

SHLIB_LINK += -l:pgcrypto.so

PG_CONFIG ?= pg_config
PGXS := $(shell $(PG_CONFIG) --pgxs)
include $(PGXS)

tdeforpg--1.0.sql: \
	SOURCES/lib/init/cipher_definition.sql \
	SOURCES/lib/init/cipher_key_function.sql \
	SOURCES/lib/init/common_session_create.sql \
	SOURCES/lib/init/pgtde_parallel_safe_setting.sql
	cat $^ > $@

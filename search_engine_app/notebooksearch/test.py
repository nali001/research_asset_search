from notebooksearch import postgres_tools
# commands = ['BEGIN;', 
# 'CREATE TABLE "notebooksearch_cellcontent" ("id" bigserial NOT NULL PRIMARY KEY, "cell_type" varchar(60) NOT NULL, "cell_content" text NOT NULL, "query_generation_log_id" bigint NOT NULL);', 
# 'ALTER TABLE "notebooksearch_cellcontent" ADD CONSTRAINT "notebooksearch_cellc_query_generation_log_d1ec8f24_fk_notebooks" FOREIGN KEY ("query_generation_log_id") REFERENCES "notebooksearch_querygenerationlog" ("id") DEFERRABLE INITIALLY DEFERRED;', 
# 'CREATE INDEX "notebooksearch_cellcontent_query_generation_log_id_d1ec8f24" ON "notebooksearch_cellcontent" ("query_generation_log_id");', 
# 'COMMIT;']

commands = ["""
UPDATE django_migrations SET app="notebooksearch" WHERE app="notebooksearch"; 
"""]
postgres_tools.create_tables(commands)

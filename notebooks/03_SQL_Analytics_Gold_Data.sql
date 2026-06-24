-- Databricks notebook source
-- MAGIC %python
-- MAGIC # Gold Layer Analytics
-- MAGIC
-- MAGIC df_gold = spark.read.parquet(
-- MAGIC     "abfss://gold@stnenimadlsdev01.dfs.core.windows.net/state_revenue_summary"
-- MAGIC )
-- MAGIC
-- MAGIC df_gold.createOrReplaceTempView("state_revenue")
-- MAGIC
-- MAGIC df_gold.show()
-- MAGIC print("state_revenue view created")

-- COMMAND ----------

SELECT *
FROM state_revenue
ORDER BY TotalRevenue DESC;
# Databricks notebook source
print("Cluster OK")
print(spark.version)

# COMMAND ----------

spark.range(5).show()

# COMMAND ----------

dbutils.fs.ls("/")

# COMMAND ----------

# ADLS authentication is configured outside this notebook for security.
# Storage key intentionally removed before GitHub export.

# COMMAND ----------

df_sales = spark.read.option("header", "true").csv(
    "abfss://bronze@stnenimadlsdev01.dfs.core.windows.net/sales.csv"
)

df_sales.show()

# COMMAND ----------

from pyspark.sql.functions import col, upper, to_date

df_sales_silver = (
    df_sales
    .withColumn("OrderID", col("OrderID").cast("int"))
    .withColumn("Quantity", col("Quantity").cast("int"))
    .withColumn("UnitPrice", col("UnitPrice").cast("double"))
    .withColumn("Revenue", col("Quantity") * col("UnitPrice"))
    .withColumn("Category", upper(col("Category")))
    .withColumn("OrderDate", to_date(col("OrderDate"), "yyyy-MM-dd"))
)

df_sales_silver.show()
df_sales_silver.printSchema()

# COMMAND ----------

df_sales_silver.write.mode("overwrite").parquet(
    "abfss://silver@stnenimadlsdev01.dfs.core.windows.net/sales_cleaned"
)

# COMMAND ----------

dbutils.fs.ls(
    "abfss://silver@stnenimadlsdev01.dfs.core.windows.net/"
)

# COMMAND ----------

from pyspark.sql.functions import sum

df_sales_gold = (
    df_sales_silver
    .groupBy("State")
    .agg(
        sum("Revenue").alias("TotalRevenue")
    )
)

df_sales_gold.show()

# COMMAND ----------

df_sales_gold.write.mode("overwrite").parquet(
    "abfss://gold@stnenimadlsdev01.dfs.core.windows.net/state_revenue_summary"
)

# COMMAND ----------

dbutils.fs.ls(
    "abfss://gold@stnenimadlsdev01.dfs.core.windows.net/"
)

# COMMAND ----------

# ADLS authentication configured externally.
# Storage key removed before GitHub export.
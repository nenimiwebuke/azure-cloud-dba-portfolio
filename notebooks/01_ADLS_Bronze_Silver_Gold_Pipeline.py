# Databricks notebook source
# ADLS authentication is configured outside the notebook for security.

# COMMAND ----------

df = spark.read.option("header", "true").csv(
    "abfss://bronze@stnenimadlsdev01.dfs.core.windows.net/employees.csv"
)

df.show()

# COMMAND ----------

from pyspark.sql.functions import col, upper

df_silver = (
    df
    .withColumn("EmployeeID", col("EmployeeID").cast("int"))
    .withColumn("Salary", col("Salary").cast("int"))
    .withColumn("Department", upper(col("Department")))
)

df_silver.show()
df_silver.printSchema()

# COMMAND ----------

df_silver.write.mode("overwrite").parquet(
    "abfss://silver@stnenimadlsdev01.dfs.core.windows.net/employees_cleaned"
)

# COMMAND ----------

dbutils.fs.ls("abfss://silver@stnenimadlsdev01.dfs.core.windows.net/")

# COMMAND ----------

from pyspark.sql.functions import avg, count

df_gold = (
    df_silver
    .groupBy("Department")
    .agg(
        count("*").alias("EmployeeCount"),
        avg("Salary").alias("AverageSalary")
    )
)

df_gold.show()


# COMMAND ----------

df_gold.write.mode("overwrite").parquet(
    "abfss://gold@stnenimadlsdev01.dfs.core.windows.net/employee_summary"
)

# COMMAND ----------

dbutils.fs.ls(
    "abfss://gold@stnenimadlsdev01.dfs.core.windows.net/"
)

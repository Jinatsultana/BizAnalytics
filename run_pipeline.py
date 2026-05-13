# ============================================================
# run_pipeline.py — Master pipeline orchestrator
# Run this single file to execute the full pipeline end-to-end
# ============================================================

import time
from utils import setup_logger
from data_cleaning       import run_cleaning
from feature_engineering import run_feature_engineering
from db_loader           import run_db_load

logger = setup_logger("pipeline")


def main():
    logger.info("=" * 60)
    logger.info("  Customer Behaviour Analysis — Production Pipeline")
    logger.info("=" * 60)
    start = time.time()

    try:
        # Step 1 — Clean raw data
        logger.info("\n[STEP 1/3] Data Cleaning")
        df = run_cleaning()

        # Step 2 — Feature engineering (RFM, CLV, Churn, Clusters)
        logger.info("\n[STEP 2/3] Feature Engineering")
        df = run_feature_engineering(df)

        # Step 3 — Load to SQL Server + create views
        logger.info("\n[STEP 3/3] Database Load")
        run_db_load(df)

        elapsed = time.time() - start
        logger.info(f"\n{'='*60}")
        logger.info(f"  Pipeline complete in {elapsed:.1f}s")
        logger.info(f"  Rows processed: {len(df):,}")
        logger.info(f"  New columns added: rfm_score, rfm_segment, rfm_total,")
        logger.info(f"                     clv, clv_discounted, clv_tier,")
        logger.info(f"                     churn_risk, churn_risk_score,")
        logger.info(f"                     customer_segment, cluster_id")
        logger.info(f"  SQL views created: vw_rfm_segments, vw_clv_analysis,")
        logger.info(f"                     vw_churn_risk, vw_category_revenue")
        logger.info(f"{'='*60}")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()

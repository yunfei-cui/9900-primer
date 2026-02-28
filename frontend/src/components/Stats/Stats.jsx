import './styles.module.css'
import styles from './styles.module.css'

export default function Stats({ stats }) {
  return (
    <div className={styles.statsContainer}>
      <div className={styles.statItem}>
        <div className={styles.statLabel}>Count</div>
        <div className={styles.statValue}>{stats.count}</div>
      </div>
      <div className={styles.statItem}>
        <div className={styles.statLabel}>Average</div>
        <div className={styles.statValue}>{stats.average}</div>
      </div>
      <div className={styles.statItem}>
        <div className={styles.statLabel}>Minimum</div>
        <div className={styles.statValue}>{stats.min ?? '-'}</div>
      </div>
      <div className={styles.statItem}>
        <div className={styles.statLabel}>Maximum</div>
        <div className={styles.statValue}>{stats.max ?? '-'}</div>
      </div>
    </div>
  )
}

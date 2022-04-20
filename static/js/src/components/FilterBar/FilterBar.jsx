import styles from './FilterBar.css';

export default function FilterBar({getViewFromFilter}){
  return (
    <nav>
      <ul className={styles.nav}>
        <li><button onClick={() => getViewFromFilter('books')}>Books</button></li>
        <li><button onClick={() => getViewFromFilter('publishers')}>Publishers</button></li>
      </ul>
    </nav>
  );
}

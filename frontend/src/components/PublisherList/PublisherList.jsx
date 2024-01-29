import PropTypes from '../PropTypes';

import { PublisherItem } from '../PublisherItem/PublisherItem';

import styles from './PublisherList.css';

export const PublisherList = props => {
  const { publishers } = props;

  return (
    <div>
      <h1>Publishers</h1>
      <ol className={styles.list}>
        {publishers.map(publisher => (
          <li key={publisher.pk}>
            <PublisherItem publisher={publisher} />
          </li>
        ))}
      </ol>
    </div>
  );
};

PublisherList.propTypes = {
  publishers: PropTypes.publisherList,
};

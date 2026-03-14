import { useState } from 'react';
import { FaHeart } from 'react-icons/fa';

import './HeartIcon.css';

function HeartIcon({initialValue = true, onClick}) {
  const [favourite, setFavourite] = useState(initialValue);

  const onHeartClick = () => {
    setFavourite(!favourite);
    if (onClick) onClick(!favourite);
  }

  return (
    <div
      style={{
        borderRadius: '50%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <FaHeart
        color={favourite ? "red" : "gray"}
        size={30}
        onClick={onHeartClick}
        className='heart-icon'
      />
    </div>
  );
}

export default HeartIcon;
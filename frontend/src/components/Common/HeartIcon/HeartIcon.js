import { useState } from 'react';
import { FaHeart } from 'react-icons/fa';

import './HeartIcon.css';

function HeartIcon({initialValue = true, onClick}) {
  const [liked, setLiked] = useState(initialValue);

  const onHeartClick = () => {
    setLiked(!liked);
    if (onClick) onClick(!liked);
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
        color={liked ? "red" : "gray"}
        size={30}
        onClick={onHeartClick}
        className='heart-icon'
      />
    </div>
  );
}

export default HeartIcon;
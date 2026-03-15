import React, { useState } from "react";
import { FaListUl } from "react-icons/fa";

import './WishlistIcon.css';

function WishlistIcon({initialValue = false, onClick}){
    const [wishlist, setWishlist] = useState(initialValue);

    const onWishlistClick = () => {
        setWishlist(!wishlist);
        if (onClick) onClick(!wishlist)
    }

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <FaListUl
        color={wishlist ? "orange" : "gray"}
        size={30}
        onClick={onWishlistClick}
        className='wishlist'
      />
    </div>
  );
}

export default WishlistIcon;
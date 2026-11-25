import {describe, expect, it, jest} from "@jest/globals";
import {render, screen} from "@testing-library/react";
import {MemoryRouter} from "react-router-dom";
import AlbumActions from "./AlbumActions";


jest.mock('../Common/WishlistIcon/WishlistIcon', () => () => (
    <div data-testid="wishlist-icon">WishlistIcon mock</div>
));
jest.mock('../Common/HeartIcon/HeartIcon', () => () => (
    <div data-testid="heart-icon">HeartIcon mock</div>
));
jest.mock('../Common/Headphones/Headphones', () => () => (
    <div data-testid="headphones-icon">Headphones mock</div>
));

describe("AlbumActions component", () => {
    const userAlbumData = {
        favourite: true,
        listened: false,
        wishlist: false,
    };
    const mockHandlers = {
        onWishlickClick: jest.fn(),
        onFavouriteClick: jest.fn(),
        onListenedClick: jest.fn(),
    }

    const renderComponent = (props = {}) => {
        return render(
            <MemoryRouter>
                <AlbumActions
                    isAuthenticated={true}
                    userAlbumData={userAlbumData}
                    {...mockHandlers}
                    {...props}
                />
            </MemoryRouter>
        );
    }

    it('should render actions if user is authenticated', () => {
        renderComponent();

        const wishlistIcon = screen.getByTestId("wishlist-icon");
        expect(wishlistIcon).toBeInTheDocument();

        const heartIcon = screen.getByTestId("heart-icon");
        expect(heartIcon).toBeInTheDocument();

        const headphonesIcon = screen.getByTestId("headphones-icon");
        expect(headphonesIcon).toBeInTheDocument();
    });
    it('should not render actions if user is not authenticated', () => {
        renderComponent({isAuthenticated: false});

        const wishlistIcon = screen.queryByTestId("wishlist-icon");
        expect(wishlistIcon).not.toBeInTheDocument();

        const heartIcon = screen.queryByTestId("heart-icon");
        expect(heartIcon).not.toBeInTheDocument();

        const headphonesIcon = screen.queryByTestId("headphones-icon");
        expect(headphonesIcon).not.toBeInTheDocument();
    });
});
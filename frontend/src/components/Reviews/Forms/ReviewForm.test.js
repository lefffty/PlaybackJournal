import {describe, expect, it, jest, beforeEach} from "@jest/globals";
import "@testing-library/jest-dom";
import {render, screen, waitFor} from "@testing-library/react";
import {MemoryRouter} from "react-router-dom";
import userEvent from "@testing-library/user-event";

import AxiosInstance from "../../AxiosInstance";
import ReviewForm from "./ReviewForm";

jest.mock("../../AxiosInstance");

describe("ReviewForm component", () => {
    const albumId = 1;
    const mockOnReviewAdded = jest.fn();

    const renderComponent = (props = {}) => {
        return (
            render(
                <MemoryRouter>
                    <ReviewForm
                        albumId={albumId}
                        onReviewAdded={mockOnReviewAdded}
                        {...props}
                    />
                </MemoryRouter>
            )
        )
    }

    beforeEach(() => {
        renderComponent();
    })

    it('should render all form fields correctly', () => {
        expect(screen.getByTestId("review-title"));
        expect(screen.getByTestId("review-title-control"));
        expect(screen.getByTestId("review-type"));
        expect(screen.getByTestId("review-type-control"));
        expect(screen.getByTestId("review-text"));
        expect(screen.getByTestId("review-text-control"));
        expect(screen.getByTestId("review-submit-btn"));
    });

    it('should correctly send request when submitting form', async () => {
        AxiosInstance.post.mockResolvedValueOnce({data: {}});

        userEvent.type(screen.getByTestId("review-title-control"), "Text title");
        userEvent.selectOptions(screen.getByTestId("review-type-control"), "positive");
        userEvent.type(screen.getByTestId("review-text-control"), "Text text");
        userEvent.click(screen.getByTestId("review-submit-btn"));

        await waitFor(() => {
            expect(AxiosInstance.post).toHaveBeenCalledWith("/api/reviews/", {
                title: 'Text title',
                text: 'Text text',
                type: 'positive',
                album: albumId,
            });
        });

        expect(mockOnReviewAdded).toHaveBeenCalledTimes(1);
    });
})
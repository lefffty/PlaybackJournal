import React from "react";
import { ButtonGroup, Button } from "react-bootstrap";

const Pagination = ({
    minPage,
    maxPage,
    currentPage,
    previousPage,
    nextPage,
    onFirstPageClick,
    onPreviousPageClick,
    onNextPageClick,
    onLastPageClick
}) => {

    const handleFirstPageClick = () => {
        onFirstPageClick();
    }

    const handlePreviousPageClick = () => {
        onPreviousPageClick();
    }

    const handleNextPageClick = () => {
        onNextPageClick();
    }

    const handleLastPageClick = () => {
        onLastPageClick();
    }

    return (
        <div className="justify-content-center d-flex mb-3">
            <ButtonGroup>
                {minPage !== (currentPage - 1) && minPage !== currentPage ? (
                    <>
                        <Button variant="secondary" onClick={handleFirstPageClick}>
                            First
                        </Button>
                    </>
                ) : (
                    <>
                    </>
                )}
                {previousPage !== null ? (
                    <>
                        <Button variant="primary" onClick={handlePreviousPageClick}>
                            {currentPage - 1}
                        </Button>
                    </>
                ) : (
                    <>
                    </>
                )}
                <Button variant="success">
                    {currentPage}
                </Button>
                {nextPage !== null ? (
                    <>
                        <Button variant="primary" onClick={handleNextPageClick}>
                            {currentPage + 1}
                        </Button>
                    </>
                ) : (
                    <>
                    </>
                )}
                {currentPage !== maxPage && (currentPage + 1) !== maxPage ? (
                    <>
                        <Button variant="secondary" onClick={handleLastPageClick}>
                            Last
                        </Button>
                    </>
                ) : (
                    <>
                    </>
                )}
            </ButtonGroup>
        </div>
    )
}

export default Pagination;
import { compose, createStore, applyMiddleware, combineReducers } from 'redux';
import thunk from 'redux-thunk';
import { routerMiddleware, routerReducer } from 'react-router-redux';

// custom reducers

const configureStore = (history) => {
  const reducerObj = {
    routing: routerReducer
  };
  const reducers = combineReducers(reducerObj);
  const store = createStore(
    reducers,
    compose(applyMiddleware(thunk), applyMiddleware(routerMiddleware(history)))
  );
  return store;
};

export default configureStore;

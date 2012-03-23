% Cry Detector Training

data = load('data.txt');

% Split data to train, test and crossvalidation sets
total_count = size(data,1);
data = data(randperm(total_count), :);

train_count = int32(total_count*0.6);
test_count = int32(total_count*0.2);
cv_count = total_count - train_count - test_count;


Xtrain = data(1:train_count, 1:128);
ytrain = data(1:train_count, 129);

Xtest = data(train_count+1:train_count+test_count, 1:128);
ytest = data(train_count+1:train_count+test_count, 129);
rtest = data(train_count+1:train_count+test_count, 130);

Xval = data(train_count+test_count+1:total_count, 1:128);
yval = data(train_count+test_count+1:total_count, 129);

X = Xtrain;
y = ytrain;

% Xval = featureNormalize(Xval);
% yval = featureNormalize(yval);

#lambda_vec = [0, 0.1, 0.5, 1, 10, 50, 100 1000 5000 10000 30000 50000 60000 100000]';
lambda_vec = [1000 5000 10000 30000]';
#error_train = zeros(length(lambda_vec), 1);
#error_val = zeros(length(lambda_vec), 1);

[m, n] = size(X);
X = [ones(m, 1) X];                % Add intercept term to X
Xval = [ones(cv_count, 1) Xval];                % Add intercept term to Xval
Xtest = [ones(test_count, 1) Xtest];

% Compute and display initial cost and gradient
initial_theta = zeros(n + 1, 1); % Initialize fitting parameters
[cost, grad] = costFunctionReg(initial_theta, X, y, 0);
fprintf('Cost at initial theta (zeros): %f\n', cost);

options = optimset('GradObj', 'on', 'MaxIter', 400);
[theta, cost] = fminunc(@(t)(costFunctionReg(t, X, y, 0)), initial_theta, options);

% error_train = zeros(size(1:50:m,2), 1);
% error_val   = zeros(size(1:50:m,2), 1);
% for k=1:50:m
%    fprintf('%d\n', k);
%    Xtrain = X(1:k,:);
%    ytrain = y(1:k);
%    [theta, cost] = fminunc(@(t)(costFunctionReg(t, Xtrain, ytrain, 0)), initial_theta, options);
%    error_train(int32(k/50)+1) = 100 * (1 - mean(predict(theta, Xtrain) == ytrain));
%    error_val(int32(k/50)+1) = 100 * (1 - mean(predict(theta, Xval) == yval));
%end

% plot(1:50:m, error_train, 1:50:m, error_val);
% title('Learning curve for linear regression')
% legend('Train', 'Cross Validation')
% xlabel('Number of training examples')
% ylabel('Error')

% Selecting right lambda
% options = optimset('GradObj', 'on', 'MaxIter', 10000);
% for k = 1:length(lambda_vec)
%   lambda = lambda_vec(k);
%   [theta, cost] = fminunc(@(t)(costFunctionReg(t, X, y, lambda)), initial_theta, options);
%  error_train(k) = 100 * (1 - mean(predict(theta, X) == y));
%  error_val(k) = 100 * (1 - mean(predict(theta, Xval) == yval));
%  error_train(k)
%  error_val(k)
%  fprintf('%f Cost at theta found by fminunc: %f\n', lambda, cost);
%end

% plot(lambda_vec, error_train, lambda_vec, error_val);
% title('Learning curve for linear regression')
% legend('Train', 'Cross Validation')
% xlabel('lambda')
% ylabel('Error')


% Compute accuracy on our training set
p = predict(theta, Xtest);

fprintf('Train Accuracy: %f \n', mean(double(p == ytest)) * 100);
fprintf('Total size %d \n', length(rtest == 1));
fprintf('Total right predicted %d \n', sum(predict(theta, Xtest) == ytest));
fprintf('Right predicted cries: %f \n', sum((predict(theta, Xtest) == ytest)(ytest==1)));
fprintf('Right predicted nocries: %f \n', sum((predict(theta, Xtest) == ytest)(ytest==0)));
fprintf('Not predicted cries: %f \n', sum((predict(theta, Xtest) != ytest)(ytest==1)));
fprintf('Wrong predicted cries: %f \n', sum((predict(theta, Xtest) != ytest)(ytest==0)));
fprintf('Total Cry %d\n', sum(ytest));
fprintf('Total NoCry %d\n', sum(ytest==0));
pause

theta

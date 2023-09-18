<?php

require(__DIR__ . '/vendor/autoload.php');

use Captioning\Format\SubripFile;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Console\SingleCommandApplication;

(new SingleCommandApplication())
    ->setName('merge')
    ->addArgument('output', InputArgument::REQUIRED)
    ->addArgument('input', InputArgument::IS_ARRAY)
    ->setCode(function (InputInterface $input, OutputInterface $output): int {
        $inputFilenames = $input->getArgument('input');

        $initial = new SubripFile(array_shift($inputFilenames), _requireStrictFileFormat: true);

        $merged = array_reduce(
            $inputFilenames,
            fn ($merged, string $filename) => $merged->merge(new SubripFile($filename)),
            $initial
        );

        $merged->build()->save($input->getArgument('output'));

        return Command::SUCCESS;
    })
    ->run();
